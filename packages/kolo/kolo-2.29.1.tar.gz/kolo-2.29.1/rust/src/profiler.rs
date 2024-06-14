use bstr::Finder;
use hashbrown::HashMap;
use pyo3::exceptions::PyAttributeError;
use pyo3::ffi;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use pyo3::types::PyDict;
use pyo3::types::PyFrame;
use std::borrow::Cow;
use std::cell::RefCell;
use std::os::raw::c_int;
use std::sync::Mutex;
use thread_local::ThreadLocal;
use ulid::Ulid;

use super::filters;
use super::plugins::{load_plugins, PluginProcessor};
use super::utils;
use super::utils::SerializedFrame;

#[pyclass(module = "kolo._kolo")]
pub struct KoloProfiler {
    db_path: String,
    one_trace_per_test: bool,
    trace_id: Mutex<String>,
    frames_of_interest: Mutex<Vec<SerializedFrame>>,
    frames: Mutex<HashMap<usize, Vec<SerializedFrame>>>,
    include_frames: Vec<Finder<'static>>,
    ignore_frames: Vec<Finder<'static>>,
    default_include_frames: Mutex<HashMap<String, Vec<PluginProcessor>>>,
    call_frames: ThreadLocal<RefCell<Vec<(PyObject, String)>>>,
    timestamp: f64,
    _frame_ids: ThreadLocal<RefCell<HashMap<usize, String>>>,
    current_thread: ThreadLocal<(String, Option<usize>)>,
    main_thread_id: Option<usize>,
    source: String,
    timeout: usize,
    use_threading: bool,
    lightweight_repr: bool,
}

#[pymethods]
impl KoloProfiler {
    fn save_request_in_db(&self) -> Result<(), PyErr> {
        Python::with_gil(|py| self.save_in_db(py))
    }

    fn build_trace(&self) -> Result<Py<PyBytes>, PyErr> {
        Python::with_gil(|py| self.build_trace_inner(py))
    }

    fn register_threading_profiler(
        slf: PyRef<'_, Self>,
        _frame: PyObject,
        _event: PyObject,
        _arg: PyObject,
    ) -> Result<(), PyErr> {
        // Safety:
        //
        // PyEval_SetProfile takes two arguments:
        //  * trace_func: Option<Py_tracefunc>
        //  * arg1:       *mut PyObject
        //
        // `profile_callback` matches the signature of a `Py_tracefunc`, so we only
        // need to wrap it in `Some`.
        // `slf.into_ptr()` is a pointer to our Rust profiler instance as a Python
        // object.
        //
        // We must also hold the GIL, which we do because we're called from python.
        //
        // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/fn.PyEval_SetProfile.html
        // https://docs.python.org/3/c-api/init.html#c.PyEval_SetProfile
        unsafe {
            ffi::PyEval_SetProfile(Some(profile_callback), slf.into_ptr());
        }
        Ok(())
    }
}

impl KoloProfiler {
    pub fn new_from_python(py: Python, py_profiler: &Bound<'_, PyAny>) -> Result<Self, PyErr> {
        let config = py_profiler.getattr(intern!(py, "config"))?;
        let config = config.downcast::<PyDict>()?;
        let filters = config
            .get_item("filters")
            .expect("config.get(\"filters\" should not raise.");
        let include_frames = match &filters {
            Some(filters) => match filters.get_item("include_frames") {
                Ok(include_frames) => {
                    filters::build_finders(include_frames.extract::<Vec<String>>()?)
                }
                Err(_) => Vec::new(),
            },
            None => Vec::new(),
        };
        let ignore_frames = match &filters {
            Some(filters) => match filters.get_item("ignore_frames") {
                Ok(ignore_frames) => {
                    filters::build_finders(ignore_frames.extract::<Vec<String>>()?)
                }
                Err(_) => Vec::new(),
            },
            None => Vec::new(),
        };
        let threading = PyModule::import_bound(py, "threading")?;
        let main_thread = threading.call_method0(intern!(py, "main_thread"))?;
        let main_thread_id = match main_thread.getattr(intern!(py, "native_id")) {
            Ok(main_thread_id) => main_thread_id.extract()?,
            Err(err) if err.is_instance_of::<PyAttributeError>(py) => None,
            Err(err) => return Err(err),
        };

        let timeout = match config
            .get_item("sqlite_busy_timeout")
            .expect("config.get(\"sqlite_busy_timeout\" should not raise.")
        {
            Some(timeout) => timeout.extract()?,
            None => 60,
        };
        let use_threading = match config
            .get_item("threading")
            .expect("config.get(\"threading\" should not raise.")
        {
            Some(threading) => threading.extract::<bool>().unwrap_or(false),
            None => false,
        };
        let lightweight_repr = match config
            .get_item("lightweight_repr")
            .expect("config.get(\"lightweight_repr\" should not raise.")
        {
            Some(lightweight_repr) => lightweight_repr.extract::<bool>().unwrap_or(false),
            None => false,
        };

        let default_include_frames = load_plugins(py, config)?;
        Ok(Self {
            db_path: py_profiler
                .getattr(intern!(py, "db_path"))?
                .str()?
                .extract()?,
            one_trace_per_test: py_profiler
                .getattr(intern!(py, "one_trace_per_test"))?
                .extract()?,
            trace_id: py_profiler
                .getattr(intern!(py, "trace_id"))?
                .extract::<String>()?
                .into(),
            source: py_profiler
                .getattr(intern!(py, "source"))?
                .extract::<String>()?,
            frames: HashMap::new().into(),
            frames_of_interest: Vec::new().into(),
            include_frames,
            ignore_frames,
            default_include_frames: default_include_frames.into(),
            call_frames: ThreadLocal::new(),
            timestamp: utils::timestamp(),
            _frame_ids: ThreadLocal::new(),
            current_thread: ThreadLocal::new(),
            main_thread_id,
            timeout,
            use_threading,
            lightweight_repr,
        })
    }

    fn write_argv(&self, buf: &mut Vec<u8>, argv: Vec<String>) {
        rmp::encode::write_str(buf, "command_line_args").expect("Writing to memory, not I/O");
        rmp::encode::write_array_len(buf, argv.len() as u32).expect("Writing to memory, not I/O");
        for arg in argv {
            rmp::encode::write_str(buf, &arg).expect("Writing to memory, not I/O");
        }
    }

    fn write_frames(&self, buf: &mut Vec<u8>, frames: HashMap<usize, Vec<SerializedFrame>>) {
        rmp::encode::write_str(buf, "frames").expect("Writing to memory, not I/O");
        rmp::encode::write_map_len(buf, frames.len() as u32).expect("Writing to memory, not I/O");
        for (thread_id, frames) in frames {
            rmp::encode::write_uint(buf, thread_id as u64).expect("Writing to memory, not I/O");
            utils::write_raw_frames(buf, frames);
        }
    }

    fn write_frames_of_interest(
        &self,
        buf: &mut Vec<u8>,
        frames_of_interest: Vec<SerializedFrame>,
    ) {
        rmp::encode::write_str(buf, "frames_of_interest").expect("Writing to memory, not I/O");
        utils::write_raw_frames(buf, frames_of_interest);
    }

    fn write_meta(&self, buf: &mut Vec<u8>, version: &str, source: &str) {
        rmp::encode::write_str(buf, "meta").expect("Writing to memory, not I/O");
        rmp::encode::write_map_len(buf, 3).expect("Writing to memory, not I/O");

        utils::write_str_pair(buf, "version", Some(version));
        utils::write_str_pair(buf, "source", Some(source));
        utils::write_bool_pair(buf, "use_frame_boundaries", true);
    }

    fn build_trace_inner(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        let version = PyModule::import_bound(py, "kolo.version")?
            .getattr(intern!(py, "__version__"))?
            .extract::<String>()?;
        let commit_sha = PyModule::import_bound(py, "kolo.git")?
            .getattr(intern!(py, "COMMIT_SHA"))?
            .extract::<Option<String>>()?;
        let argv = PyModule::import_bound(py, "sys")?
            .getattr(intern!(py, "argv"))?
            .extract::<Vec<String>>()?;
        let mut state = self.frames_of_interest.lock().unwrap();
        let frames_of_interest = std::mem::take(&mut *state);
        let mut state = self.frames.lock().unwrap();
        let frames = std::mem::take(&mut *state);

        let trace_id = self.trace_id.lock().unwrap().clone();
        let mut buf: Vec<u8> = vec![];

        rmp::encode::write_map_len(&mut buf, 8).expect("Writing to memory, not I/O");
        self.write_argv(&mut buf, argv);
        utils::write_str_pair(&mut buf, "current_commit_sha", commit_sha.as_deref());
        self.write_frames(&mut buf, frames);
        self.write_frames_of_interest(&mut buf, frames_of_interest);
        utils::write_int_pair(&mut buf, "main_thread_id", self.main_thread_id);
        self.write_meta(&mut buf, &version, &self.source);
        utils::write_f64_pair(&mut buf, "timestamp", self.timestamp);
        utils::write_str_pair(&mut buf, "trace_id", Some(&trace_id));

        Ok(PyBytes::new_bound(py, &buf).unbind())
    }

    fn save_in_db(&self, py: Python) -> Result<(), PyErr> {
        let kwargs = PyDict::new_bound(py);
        kwargs.set_item("timeout", self.timeout).unwrap();

        let data = self.build_trace_inner(py)?;
        kwargs.set_item("msgpack", data).unwrap();

        let trace_id = self.trace_id.lock().unwrap().clone();
        let db = PyModule::import_bound(py, "kolo.db")?;
        let save = db.getattr(intern!(py, "save_trace_in_sqlite"))?;
        save.call((&self.db_path, &trace_id), Some(&kwargs))?;
        Ok(())
    }

    fn process_frame(
        &self,
        pyframe: &Bound<'_, PyFrame>,
        event: &str,
        arg: PyObject,
        name: &str,
        frame_types: &mut Vec<String>,
        frames: &mut Vec<SerializedFrame>,
    ) -> Result<(), PyErr> {
        let py = pyframe.py();
        let (thread_name, native_id) = self
            .current_thread
            .get_or_try(|| utils::current_thread(py))?;
        let arg = arg.downcast_bound::<PyAny>(py)?;
        let pyframe_id = pyframe.as_ptr() as usize;
        let path = utils::frame_path(pyframe, py)?;
        let qualname = utils::get_qualname(pyframe, py)?;
        let locals = pyframe.getattr(intern!(py, "f_locals"))?;
        let locals = locals.downcast_into::<PyDict>().unwrap();
        let locals = match locals
            .get_item("__builtins__")
            .expect("locals.get(\"__builtins__\") should not raise.")
        {
            Some(_) => {
                let locals = locals.copy().unwrap();
                locals.del_item("__builtins__").unwrap();
                locals
            }
            None => locals,
        };
        let frame_id = self.get_and_set_frame_id(event, pyframe_id);
        let user_code_call_site = match utils::user_code_call_site(
            py,
            self.call_frames.get_or_default().borrow().to_vec(),
            frame_id.as_deref(),
        )? {
            Some(user_code_call_site) => rmpv::Value::Map(vec![
                (
                    "call_frame_id".into(),
                    user_code_call_site.call_frame_id.into(),
                ),
                ("line_number".into(), user_code_call_site.line_number.into()),
            ]),
            None => rmpv::Value::Nil,
        };
        let mut arg = match self.lightweight_repr {
            true => utils::dump_msgpack_lightweight_repr(py, arg)?,
            false => utils::dump_msgpack(py, arg)?,
        };
        let mut locals = match self.lightweight_repr {
            true => utils::dump_msgpack_lightweight_repr(py, &locals)?,
            false => utils::dump_msgpack(py, &locals)?,
        };

        self.update_call_frames(event, pyframe, frame_id.as_deref());

        let mut buf: Vec<u8> = vec![];

        rmp::encode::write_map_len(&mut buf, 12).expect("Writing to memory, not I/O");

        utils::write_str_pair(&mut buf, "path", Some(&path));
        utils::write_str_pair(&mut buf, "co_name", Some(name));
        utils::write_str_pair(&mut buf, "qualname", qualname.as_deref());
        utils::write_str_pair(&mut buf, "event", Some(event));
        utils::write_str_pair(&mut buf, "frame_id", frame_id.as_deref());
        utils::write_raw_pair(&mut buf, "arg", &mut arg);
        utils::write_raw_pair(&mut buf, "locals", &mut locals);
        utils::write_str_pair(&mut buf, "thread", Some(thread_name));
        utils::write_int_pair(&mut buf, "thread_native_id", *native_id);
        utils::write_f64_pair(&mut buf, "timestamp", utils::timestamp());
        utils::write_str_pair(&mut buf, "type", Some("frame"));

        rmp::encode::write_str(&mut buf, "user_code_call_site")
            .expect("Writing to memory, not I/O");
        rmpv::encode::write_value(&mut buf, &user_code_call_site).unwrap();

        frames.push(buf);
        frame_types.push("frame".to_string());
        self.push_frames(py, event, frame_types, frames)
    }

    fn get_and_set_frame_id(&self, event: &str, pyframe_id: usize) -> Option<String> {
        match event {
            "call" => {
                let frame_id = utils::frame_id();
                self._frame_ids
                    .get_or_default()
                    .borrow_mut()
                    .insert(pyframe_id, frame_id.clone());
                Some(frame_id)
            }
            "return" => self
                ._frame_ids
                .get_or_default()
                .borrow()
                .get(&pyframe_id)
                .cloned(),
            _ => None,
        }
    }

    fn update_call_frames(&self, event: &str, frame: &Bound<'_, PyFrame>, frame_id: Option<&str>) {
        match (event, frame_id) {
            ("call", Some(frame_id)) => {
                self.call_frames
                    .get_or_default()
                    .borrow_mut()
                    .push((frame.clone().into(), frame_id.to_string()));
            }
            ("return", _) => {
                if let Some(e) = self.call_frames.get() {
                    e.borrow_mut().pop();
                }
            }
            _ => {}
        }
    }

    fn push_frames(
        &self,
        py: Python,
        event: &str,
        frame_types: &mut [String],
        frames: &mut Vec<SerializedFrame>,
    ) -> Result<(), PyErr> {
        if frame_types.is_empty() {
            return Ok(());
        }

        if event == "return" {
            frames.reverse();
            frame_types.reverse();
        }

        let (_, native_id) = self
            .current_thread
            .get_or_try(|| utils::current_thread(py))?;

        if self.one_trace_per_test {
            for (index, frame_type) in frame_types.iter().enumerate() {
                match frame_type.as_str() {
                    "start_test" => {
                        let mut before: Vec<SerializedFrame> = frames.drain(..index).collect();
                        self.push_frame_data(*native_id, &mut before);
                        self.start_test()
                    }
                    "end_test" => {
                        let mut before: Vec<SerializedFrame> = frames.drain(..index + 1).collect();
                        self.push_frame_data(*native_id, &mut before);
                        self.save_in_db(py)?;
                    }
                    _ => {}
                }
            }
        }
        self.push_frame_data(*native_id, frames);
        Ok(())
    }

    fn push_frame_data(&self, native_id: Option<usize>, frames: &mut Vec<SerializedFrame>) {
        match native_id {
            None => self.frames_of_interest.lock().unwrap().append(frames),
            Some(native_id) => {
                if !self.use_threading || Some(native_id) == self.main_thread_id {
                    self.frames_of_interest.lock().unwrap().append(frames);
                } else {
                    self.frames
                        .lock()
                        .unwrap()
                        .entry(native_id)
                        .or_default()
                        .append(frames);
                };
            }
        }
    }

    fn start_test(&self) {
        let trace_id = Ulid::new();
        let trace_id = format!("trc_{}", trace_id.to_string());
        let mut self_trace_id = self.trace_id.lock().unwrap();
        *self_trace_id = trace_id;

        let mut frames_of_interest = self.frames_of_interest.lock().unwrap();
        *frames_of_interest = vec![];
        let mut frames = self.frames.lock().unwrap();
        *frames = HashMap::new();
    }

    fn process_include_frames(&self, filename: &str) -> bool {
        self.include_frames
            .iter()
            .any(|finder| finder.find(filename).is_some())
    }

    fn process_ignore_frames(&self, filename: &str) -> bool {
        self.ignore_frames
            .iter()
            .any(|finder| finder.find(filename).is_some())
    }

    fn process_default_ignore_frames(
        &self,
        pyframe: &Bound<'_, PyFrame>,
        co_filename: &str,
    ) -> bool {
        filters::library_filter(co_filename)
            | filters::frozen_filter(co_filename)
            | filters::kolo_filter(co_filename)
            | filters::exec_filter(co_filename)
            | filters::pytest_generated_filter(co_filename)
            | filters::attrs_filter(co_filename, pyframe)
    }

    fn include_frame(&self, pyframe: &Bound<'_, PyFrame>, filename: &str) -> bool {
        self.process_include_frames(filename) | !self.ignore_frame(pyframe, filename)
    }

    fn ignore_frame(&self, pyframe: &Bound<'_, PyFrame>, filename: &str) -> bool {
        self.process_default_ignore_frames(pyframe, filename) | self.process_ignore_frames(filename)
    }

    fn run_frame_processor(
        &self,
        py: Python,
        processor: &mut PluginProcessor,
        pyframe: &Bound<'_, PyFrame>,
        event: &str,
        arg: &PyObject,
        filename: &str,
    ) -> Result<Option<(String, Vec<u8>)>, PyErr> {
        if !processor.matches(py, pyframe, event, arg, filename)? {
            return Ok(None);
        }
        let data = match processor.process(
            py,
            pyframe,
            event,
            arg,
            self.call_frames.get_or_default().borrow().clone(),
        )? {
            Some(data) => data,
            None => return Ok(None),
        };
        let frame_type = data
            .bind(py)
            .get_item("type")
            .expect("data[\"type\"] should not raise.")
            .expect("data[\"type\"] should not be missing.")
            .extract()?;

        let data = match self.lightweight_repr {
            true => utils::dump_msgpack_lightweight_repr(py, data.bind(py))?,
            false => utils::dump_msgpack(py, data.bind(py))?,
        };

        Ok(Some((frame_type, data)))
    }

    fn profile(&self, frame: &PyObject, arg: PyObject, event: &str, py: Python) {
        let pyframe = frame.bind(py);
        let pyframe = pyframe
            .downcast::<PyFrame>()
            .expect("Python gives us a PyFrame");
        let f_code = pyframe
            .getattr(intern!(py, "f_code"))
            .expect("A frame always has an `f_code`");
        let co_filename = f_code
            .getattr(intern!(py, "co_filename"))
            .expect("`f_code` always has `co_filename`");
        let co_name = f_code
            .getattr(intern!(py, "co_name"))
            .expect("`f_code` always has `co_name`");
        let filename = co_filename
            .extract::<Cow<str>>()
            .expect("`co_filename` is always a string");
        let name = co_name
            .extract::<Cow<str>>()
            .expect("`co_name` is always a string");

        let mut frames = vec![];
        let mut frame_types = vec![];
        let mut guard = self.default_include_frames.lock().unwrap();
        if let Some(processors) = guard.get_mut(&name.to_string()) {
            for processor in processors.iter_mut() {
                match self.run_frame_processor(py, processor, pyframe, event, &arg, &filename) {
                    Ok(Some((frame_type, data))) => {
                        frames.push(data);
                        frame_types.push(frame_type);
                    }
                    Ok(None) => {}
                    Err(err) => self.log_error(py, err, pyframe, event, &co_filename, &co_name),
                }
            }
        };
        // Prevent deadlock where thread 1 holds the `self.default_include_frames` guard
        // and thread 2 holds the `self.frames` or `self.frames_of_interest` guard and
        // neither thread can make progress because they are waiting for the other.
        drop(guard);

        let result = match self.include_frame(pyframe, &filename) {
            true => self.process_frame(pyframe, event, arg, &name, &mut frame_types, &mut frames),
            false => self.push_frames(py, event, &mut frame_types, &mut frames),
        };
        if let Err(err) = result {
            self.log_error(py, err, pyframe, event, &co_filename, &co_name);
        }
    }

    fn log_error(
        &self,
        py: Python,
        err: PyErr,
        pyframe: &Bound<'_, PyFrame>,
        event: &str,
        co_filename: &Bound<'_, PyAny>,
        co_name: &Bound<'_, PyAny>,
    ) {
        let logging = PyModule::import_bound(py, "logging").unwrap();
        let logger = logging.call_method1("getLogger", ("kolo",)).unwrap();
        let locals = pyframe.getattr(intern!(py, "f_locals")).unwrap();

        let kwargs = PyDict::new_bound(py);
        kwargs.set_item("exc_info", err).unwrap();

        logger
            .call_method(
                "warning",
                (
                    PYTHON_EXCEPTION_WARNING,
                    co_filename,
                    co_name,
                    event,
                    locals,
                ),
                Some(&kwargs),
            )
            .unwrap();
    }
}

const PYTHON_EXCEPTION_WARNING: &str = "Unexpected exception in Rust.
    co_filename: %s
    co_name: %s
    event: %s
    frame locals: %s
";

// Safety:
//
// We match the type signature of `Py_tracefunc`.
//
// https://docs.rs/pyo3-ffi/latest/pyo3_ffi/type.Py_tracefunc.html
pub extern "C" fn profile_callback(
    _obj: *mut ffi::PyObject,
    _frame: *mut ffi::PyFrameObject,
    what: c_int,
    _arg: *mut ffi::PyObject,
) -> c_int {
    let event = match what {
        ffi::PyTrace_CALL => "call",
        ffi::PyTrace_RETURN => "return",
        _ => return 0,
    };
    let _frame = _frame as *mut ffi::PyObject;
    Python::with_gil(|py| {
        // Safety:
        //
        // `from_borrowed_ptr_or_err` must be called in an unsafe block.
        //
        // `_obj` is a reference to our `KoloProfiler` wrapped up in a Python object, so
        // we can safely convert it from an `ffi::PyObject` to a `PyObject`.
        //
        // We borrow the object so we don't break reference counting.
        //
        // https://docs.rs/pyo3/latest/pyo3/struct.Py.html#method.from_borrowed_ptr_or_err
        // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
        let obj = match unsafe { PyObject::from_borrowed_ptr_or_err(py, _obj) } {
            Ok(obj) => obj,
            Err(err) => {
                err.restore(py);
                return -1;
            }
        };
        let profiler = match obj.extract::<PyRef<KoloProfiler>>(py) {
            Ok(profiler) => profiler,
            Err(err) => {
                err.restore(py);
                return -1;
            }
        };

        // Safety:
        //
        // `from_borrowed_ptr_or_err` must be called in an unsafe block.
        //
        // `_frame` is an `ffi::PyFrameObject` which can be converted safely
        // to a `PyObject`. We can later convert it into a `pyo3::types::PyFrame`.
        //
        // We borrow the object so we don't break reference counting.
        //
        // https://docs.rs/pyo3/latest/pyo3/struct.Py.html#method.from_borrowed_ptr_or_err
        // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
        let frame = match unsafe { PyObject::from_borrowed_ptr_or_err(py, _frame) } {
            Ok(frame) => frame,
            Err(err) => {
                err.restore(py);
                return -1;
            }
        };

        // Safety:
        //
        // `from_borrowed_ptr_or_opt` must be called in an unsafe block.
        //
        // `_arg` is either a `Py_None` (PyTrace_CALL) or any PyObject (PyTrace_RETURN) or
        // NULL (PyTrace_RETURN). The first two can be unwrapped as a PyObject. `NULL` we
        // convert to a `py.None()`.
        //
        // We borrow the object so we don't break reference counting.
        //
        // https://docs.rs/pyo3/latest/pyo3/struct.Py.html#method.from_borrowed_ptr_or_opt
        // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
        let arg = match unsafe { PyObject::from_borrowed_ptr_or_opt(py, _arg) } {
            Some(arg) => arg,
            // TODO: Perhaps better exception handling here?
            None => py.None(),
        };

        profiler.profile(&frame, arg, event, py);
        0
    })
}
