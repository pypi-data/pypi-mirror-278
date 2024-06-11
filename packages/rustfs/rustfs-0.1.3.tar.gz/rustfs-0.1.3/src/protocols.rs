use anyhow::Result;
use object_store::multipart::MultipartStore;
use object_store::{ObjectMeta, ObjectStore};

use bytes::Bytes;
use std::collections::HashMap;
use std::io::Error;

pub trait MultiPartObjectStore: ObjectStore + MultipartStore {}

impl<T: ObjectStore + MultipartStore> MultiPartObjectStore for T {}

pub type DynMultiPartObjectStore = dyn MultiPartObjectStore;

pub enum Info {
    Name(String),
    Size(usize),
    Type(String),
}

pub struct FileInfo {
    pub metadata: Option<ObjectMeta>,
    pub location: String,
    pub file_type: String,
}

pub enum ListInfo {
    Details(FileInfo),
    Location(String),
}

pub type Details = HashMap<String, Info>;

pub trait AbstractFileHandle {
    fn close(&mut self) -> Result<(), Error>;
    fn flush(&mut self) -> Result<(), Error>;
    fn readable(&self) -> bool;
    fn isatty(&self) -> bool;
    fn seekable(&self) -> bool;
    fn writable(&self) -> bool;
    fn seek(&mut self, offset: usize, whence: u8) -> Result<usize, Error>;
    fn tell(&self) -> usize;
    fn readline(&mut self) -> Result<i64, Error>;
    fn readlines(&mut self) -> Result<i64, Error>;
    fn fileno(&mut self) -> Result<i64, Error>;
    fn truncate(&mut self) -> Result<i64, Error>;
    fn write(&mut self, data: &[u8]) -> Result<i64, Error>;
    fn read(&mut self, n: i64) -> Result<Bytes, Error>;
}

pub trait Fsspec {
    /// Return dict with keys: name (full path in the FS), size (in bytes), type (file,
    /// directory, or something else) and other FS-specific keys
    async fn info(&self, path: &str) -> Result<Details>;
    async fn get(&self, rpath: &str, lpath: &str, recursive: bool) -> Result<()>;
    async fn put(&self, lpath: &str, rpath: &str, recursive: bool) -> Result<()>;
    async fn ls(&self, path: &str, detail: bool) -> Result<Vec<ListInfo>>;
    async fn is_dir(&self, path: &str) -> Result<bool>;
    fn open(&self, path: &str, mode: &str) -> Result<impl AbstractFileHandle>;
}
