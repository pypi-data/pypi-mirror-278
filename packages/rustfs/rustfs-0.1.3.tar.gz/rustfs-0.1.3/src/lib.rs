use anyhow::{Error, Result};
use file_handles::PythonFileHandle;
use object_store::aws::AmazonS3Builder;
use protocols::{Fsspec, ListInfo};
use std::path::Path;
use std::sync::Arc;

use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pyo3::types::{IntoPyDict, PyDict};

use crate::fsspec_store::FsspecStore;
use crate::protocols::Info;
pub use crate::protocols::{DynMultiPartObjectStore, MultiPartObjectStore};

mod file_handles;
mod fsspec_store;
mod protocols;

fn get_kwarg<'a, 'py, T: FromPyObject<'py>>(
    kwargs: &'py Bound<'_, PyDict>,
    key: &'a str,
) -> Option<T> {
    if let Ok(Some(value)) = kwargs.get_item(key) {
        if let Ok(value) = value.extract::<T>() {
            return Some(value);
        }
    }
    None
}

#[pyclass]
struct RustFileSystem {
    rt: tokio::runtime::Runtime,
    protocol: String,
    access_key_id: Option<String>,
    secret_access_key: Option<String>,
    region: Option<String>,
    endpoint: Option<String>,
    allow_http: Option<bool>,
}

impl RustFileSystem {
    fn build_s3_store(&self, bucket: &str) -> Arc<DynMultiPartObjectStore> {
        let s3 = AmazonS3Builder::from_env();
        let s3 = s3.with_bucket_name(bucket);
        let s3 = match &self.access_key_id {
            Some(access_key_id) => s3.with_access_key_id(access_key_id),
            None => s3,
        };
        let s3 = match &self.secret_access_key {
            Some(secret_access_key) => s3.with_secret_access_key(secret_access_key),
            None => s3,
        };
        let s3 = match &self.region {
            Some(region) => s3.with_region(region),
            None => s3.with_region("us-east-2"),
        };
        let s3 = match &self.endpoint {
            Some(endpoint) => s3.with_endpoint(endpoint),
            None => s3,
        };
        let s3 = match &self.allow_http {
            Some(allow_http) => s3.with_allow_http(*allow_http),
            None => s3,
        };
        let s3 = s3.build().expect("error creating s3");
        Arc::new(s3)
    }

    fn build_store(&self, bucket: &str) -> FsspecStore {
        match self.protocol.as_str() {
            "s3" => {
                let store = self.build_s3_store(bucket);
                FsspecStore::new(store)
            }
            _ => panic!("Unsupported protocol: {}", self.protocol),
        }
    }

    fn strip_protocol(input: &str) -> &str {
        // Find the position of "://"
        if let Some(pos) = input.find("://") {
            // Return the part after "://"
            &input[pos + 3..]
        } else {
            // Return the original input if "://" is not found
            input
        }
    }

    fn split_bucket_and_path(input: &str) -> (&str, &str) {
        // Find the position of the first '/'
        if let Some(pos) = input.find('/') {
            // Split the string into bucket and path
            let bucket = &input[..pos];
            let path = &input[pos + 1..];
            (bucket, path)
        } else {
            // If no '/' is found, the whole input is considered as the bucket
            (input, "")
        }
    }

    fn parse_path<'a>(&self, path: &'a str) -> (&'a str, &'a str) {
        let path = Self::strip_protocol(path);
        Self::split_bucket_and_path(path)
    }
}

#[pymethods]
impl RustFileSystem {
    #[new]
    #[pyo3(signature = (protocol="s3", **kwargs))]
    pub fn new(protocol: &str, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Self> {
        // let store = new_s3_store();
        match kwargs {
            Some(kwargs) => {
                let access_key_id = get_kwarg(kwargs, "access_key_id");
                let secret_access_key = get_kwarg(kwargs, "secret_access_key");
                let region = get_kwarg(kwargs, "region");
                let endpoint = get_kwarg(kwargs, "endpoint");
                let allow_http = get_kwarg(kwargs, "allow_http");
                Ok(RustFileSystem {
                    rt: tokio::runtime::Runtime::new()?,
                    protocol: protocol.to_string(),
                    access_key_id,
                    secret_access_key,
                    region,
                    endpoint,
                    allow_http,
                })
            }
            None => Ok(RustFileSystem {
                rt: tokio::runtime::Runtime::new()?,
                protocol: protocol.to_string(),
                access_key_id: None,
                secret_access_key: None,
                region: None,
                endpoint: None,
                allow_http: None,
            }),
        }
    }

    #[pyo3(signature = (path, **_py_kwargs))]
    fn is_dir(&mut self, path: &str, _py_kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<bool> {
        let (bucket, path) = self.parse_path(path);
        let store = self.build_store(bucket);
        self.rt
            .block_on(store.is_dir(path))
            .map_err(|e| PyException::new_err(e.to_string()))
    }

    #[pyo3(signature = (path, detail=false, **_py_kwargs))]
    fn ls(
        &mut self,
        path: &str,
        detail: bool,
        py: Python,
        _py_kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<PyObject> {
        let (bucket, path) = self.parse_path(path);
        let bucket_path = Path::new(bucket);
        let store: FsspecStore = self.build_store(bucket);
        let res = self
            .rt
            .block_on(store.ls(path, detail))
            .map_err(|e| PyException::new_err(e.to_string()))?;
        match detail {
            true => {
                let list: Result<Vec<PyObject>> = res
                    .iter()
                    .map(|x| match x {
                        ListInfo::Details(info) => {
                            let location = bucket_path
                                .join(&info.location)
                                .to_str()
                                .unwrap()
                                .to_string();
                            let obj_type = info.file_type.to_string();
                            let key_vals = match &info.metadata {
                                Some(metadata) => {
                                    vec![
                                        ("Key", location.to_object(py)),
                                        ("LastModified", metadata.last_modified.to_object(py)),
                                        ("size", metadata.size.to_object(py)),
                                        ("ETag", metadata.e_tag.as_ref().to_object(py)),
                                        ("name", location.to_object(py)),
                                        ("type", obj_type.to_object(py)),
                                        // ("Version", meta.version.as_ref().unwrap().to_object(py)),
                                    ]
                                }
                                None => {
                                    vec![
                                        ("Key", location.to_object(py)),
                                        ("size", 0.to_object(py)),
                                        ("name", location.to_object(py)),
                                        ("type", obj_type.to_object(py)),
                                    ]
                                }
                            };
                            Ok(key_vals.into_py_dict_bound(py).into())
                        }
                        _ => Err(Error::msg("Invalid location")),
                    })
                    .collect();
                Ok(list
                    .map_err(|e| PyException::new_err(e.to_string()))?
                    .into_py(py))
            }
            false => {
                let list: Vec<String> = res
                    .iter()
                    .map(|x| match x {
                        ListInfo::Location(location) => {
                            bucket_path.join(location).to_str().unwrap().to_string()
                        }
                        _ => panic!("Invalid location"),
                    })
                    .collect();
                Ok(list.into_py(py))
            }
        }
    }

    #[pyo3(signature = (lpath, rpath, recursive = false, **_py_kwargs))]
    fn put(
        &mut self,
        lpath: &str,
        rpath: &str,
        recursive: bool,
        _py_kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<()> {
        let (bucket, rpath) = self.parse_path(rpath);
        let store = self.build_store(bucket);
        self.rt
            .block_on(store.put(lpath, rpath, recursive))
            .map_err(|e| PyException::new_err(e.to_string()))
    }

    #[pyo3(signature = (rpath, lpath, recursive = false, **_py_kwargs))]
    fn get(
        &mut self,
        rpath: &str,
        lpath: &str,
        recursive: bool,
        _py_kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<()> {
        let (bucket, rpath) = self.parse_path(rpath);
        let store = self.build_store(bucket);
        self.rt
            .block_on(store.get(rpath, lpath, recursive))
            .map_err(|e| PyException::new_err(e.to_string()))
    }

    #[pyo3(signature = (path, mode, **_py_kwargs))]
    fn open(
        &mut self,
        path: &str,
        mode: &str,
        _py_kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<PythonFileHandle> {
        let (bucket, rpath) = self.parse_path(path);
        let store = self.build_store(bucket);
        store
            .open(rpath, mode)
            .map(PythonFileHandle::new)
            .map_err(|e| PyException::new_err(e.to_string()))
    }

    #[pyo3(signature = (path, **_py_kwargs))]
    fn info(
        &self,
        path: &str,
        py: Python,
        _py_kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<PyObject> {
        let (bucket, path) = self.parse_path(path);
        let store = self.build_store(bucket);
        let info = self
            .rt
            .block_on(store.info(path))
            .map_err(|e| PyException::new_err(e.to_string()))?;
        let size = match info.get("size") {
            Some(Info::Size(size)) => *size,
            _ => {
                Err(Error::msg("Invalid size")).map_err(|e| PyException::new_err(e.to_string()))?
            }
        };
        let name = match info.get("name") {
            Some(Info::Name(name)) => name,
            _ => {
                Err(Error::msg("Invalid name")).map_err(|e| PyException::new_err(e.to_string()))?
            }
        };
        let obj_type = match info.get("type") {
            Some(Info::Type(obj_type)) => obj_type,
            _ => {
                Err(Error::msg("Invalid type")).map_err(|e| PyException::new_err(e.to_string()))?
            }
        };

        let key_vals: Vec<(&str, PyObject)> = vec![
            ("size", size.to_object(py)),
            ("name", name.to_object(py)),
            ("type", obj_type.to_object(py)),
        ];

        Ok(key_vals.into_py_dict_bound(py).into())
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustfs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<RustFileSystem>()?;
    m.add_class::<PythonFileHandle>()?;
    Ok(())
}
