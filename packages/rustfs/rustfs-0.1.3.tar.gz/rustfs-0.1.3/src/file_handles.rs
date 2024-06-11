use crate::protocols::{AbstractFileHandle, DynMultiPartObjectStore};
use std::io::{Error, ErrorKind};
use std::sync::Arc;

use bytes::Bytes;
use object_store::path::Path;
use object_store::WriteMultipart;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use pyo3::PyErr;

#[pyclass]
pub struct PythonFileHandle {
    file_handle: FileHandle,
}

impl PythonFileHandle {
    pub fn new(file_handle: FileHandle) -> Self {
        Self { file_handle }
    }
}

#[pymethods]
impl PythonFileHandle {
    #[getter]
    fn closed(&self) -> PyResult<bool> {
        Ok(self.file_handle.closed)
    }

    #[setter]
    fn set_closed(&mut self, value: bool) {
        self.file_handle.closed = value;
    }

    fn close(&mut self) -> PyResult<()> {
        self.file_handle
            .close()
            .map_err(PyErr::new::<PyValueError, _>)
    }

    fn flush(&mut self) -> PyResult<()> {
        self.file_handle
            .flush()
            .map_err(PyErr::new::<PyValueError, _>)
    }

    fn readable(&self) -> bool {
        self.file_handle.readable()
    }

    fn isatty(&self) -> bool {
        self.file_handle.isatty()
    }

    fn seekable(&self) -> bool {
        self.file_handle.seekable()
    }

    fn writable(&self) -> bool {
        self.file_handle.writable()
    }

    fn seek(&mut self, offset: usize, whence: u8) -> PyResult<usize> {
        self.file_handle
            .seek(offset, whence)
            .map_err(PyErr::new::<PyValueError, _>)
    }

    fn tell(&self) -> usize {
        self.file_handle.tell()
    }

    fn readline(&mut self) -> PyResult<i64> {
        self.file_handle
            .readline()
            .map_err(PyErr::new::<PyValueError, _>)
    }

    fn readlines(&mut self) -> PyResult<i64> {
        self.file_handle
            .readlines()
            .map_err(PyErr::new::<PyValueError, _>)
    }

    fn fileno(&mut self) -> PyResult<i64> {
        self.file_handle
            .fileno()
            .map_err(|e| PyErr::new::<PyValueError, _>(e.to_string()))
    }

    fn truncate(&mut self) -> PyResult<i64> {
        self.file_handle
            .truncate()
            .map_err(|e| PyErr::new::<PyValueError, _>(e.to_string()))
    }

    fn write(&mut self, data: &Bound<'_, PyBytes>) -> PyResult<i64> {
        self.file_handle
            .write(data.as_bytes())
            .map_err(|e| PyErr::new::<PyValueError, _>(e.to_string()))
    }

    #[pyo3(signature = (length=-1))]
    fn read(&mut self, length: i64) -> PyResult<Py<PyBytes>> {
        let res = self.file_handle.read(length);
        if let Err(err) = res {
            return Err(PyErr::new::<PyValueError, _>(err));
        }
        Python::with_gil(|py| {
            let data = PyBytes::new_bound(py, res.as_ref().unwrap());
            Ok(Py::from(data))
        })
    }
}

#[pyclass]
pub struct FileHandle {
    path: Path,
    store: Arc<DynMultiPartObjectStore>,
    mode: String,
    size: usize,
    rt: tokio::runtime::Runtime,
    write: Option<WriteMultipart>,
    loc: usize,
    closed: bool,
}

impl FileHandle {
    pub fn new(path: Path, store: Arc<DynMultiPartObjectStore>, mode: &str) -> Self {
        let rt = tokio::runtime::Runtime::new().unwrap();

        let mut write = None;
        let mut size = 0;

        match mode {
            "wb" | "ab" => {
                let upload_ = rt.block_on(async { store.put_multipart(&path).await.unwrap() });
                write = Some(WriteMultipart::new(upload_));
            }
            _ => {
                size = rt.block_on(async { store.head(&path).await.unwrap().size });
            }
        }

        Self {
            path,
            store,
            mode: mode.to_string(),
            size,
            rt,
            write,
            loc: 0,
            closed: false,
        }
    }
}

impl AbstractFileHandle for FileHandle {
    fn close(&mut self) -> Result<(), Error> {
        if self.closed {
            return Ok(()) // see fail if return error
        }
        if self.mode == "wb" || self.mode == "ab" {
            let write_multipart = std::mem::take(&mut self.write);
            self.rt.block_on(async {
                write_multipart.unwrap().finish().await.unwrap();
            });
        }
        self.closed = true;
        Ok(())
    }

    fn flush(&mut self) -> Result<(), Error> {
        if self.mode == "wb" || self.mode == "ab" {
            self.rt.block_on(async {
                self.write
                    .as_mut()
                    .unwrap()
                    .wait_for_capacity(0)
                    .await
                    .unwrap();
            });
        }
        Ok(())
    }

    fn readable(&self) -> bool {
        self.mode == "rb" && !self.closed
    }

    // Rest of these are booleans or not implemented

    fn isatty(&self) -> bool {
        false
    }

    fn seekable(&self) -> bool {
        self.readable()
    }

    fn writable(&self) -> bool {
        return ["wb", "ab"].contains(&self.mode.as_str()) && !self.closed;
    }

    /// 0: start of file, 1: current location, 2: relative to the end
    fn seek(&mut self, offset: usize, whence: u8) -> Result<usize, Error> {
        match whence {
            0 => {
                self.loc = offset;
            }
            1 => {
                self.loc += offset;
            }
            2 => {
                self.loc = self.size + offset;
            }
            _ => {
                return Err(Error::new(
                    ErrorKind::Other,
                    format!("whence must be 0, 1, or 2, but got {}", whence),
                ))
            }
        };
        Ok(self.loc)
    }

    fn tell(&self) -> usize {
        self.loc
    }

    fn readline(&mut self) -> Result<i64, Error> {
        Err(Error::new(ErrorKind::Other, "readline not implemented"))
    }

    fn readlines(&mut self) -> Result<i64, Error> {
        Err(Error::new(ErrorKind::Other, "readlines not implemented"))
    }

    fn fileno(&mut self) -> Result<i64, Error> {
        Err(Error::new(ErrorKind::Other, "fileno not implemented"))
    }

    fn truncate(&mut self) -> Result<i64, Error> {
        Err(Error::new(ErrorKind::Other, "truncate not implemented"))
    }

    fn write(&mut self, data: &[u8]) -> Result<i64, Error> {
        if !self.writable() {
            return Err(Error::new(
                ErrorKind::Other,
                "File not opened in write mode or closed",
            ));
        }
        self.rt.block_on(async {
            self.write.as_mut().unwrap().write(data);
        });
        Ok(data.len() as i64)
    }

    fn read(&mut self, mut length: i64) -> Result<Bytes, Error> {
        if self.mode != "rb" {
            return Err(Error::new(ErrorKind::Other, "File not opened in read mode"));
        }
        if length < 0 {
            length = (self.size - self.loc) as i64;
        }
        if self.closed {
            return Err(Error::new(ErrorKind::Other, "I/O operation on closed file"));
        }
        let end = std::cmp::min(self.loc + length as usize, self.size);

        let downloaded_bytes = self
            .rt
            .block_on(async {
                self.store
                    .get_range(
                        &self.path,
                        std::ops::Range {
                            start: self.loc,
                            end,
                        },
                    )
                    .await
            })
            .unwrap();
        self.loc += downloaded_bytes.len();
        Ok(downloaded_bytes)
    }
}
