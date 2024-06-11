use anyhow::Result;
use futures::StreamExt;
use object_store::path::Path;
use std::collections::HashMap;
use std::io::SeekFrom;
use std::path::Path as StdPath;
use std::sync::Arc;
use std::{cmp, fs};

use tokio::io::{AsyncReadExt, AsyncSeekExt, AsyncWriteExt};

use crate::file_handles::FileHandle;
use crate::protocols::{Details, FileInfo, Fsspec, Info, ListInfo};
use crate::DynMultiPartObjectStore;

const CONCURRENT_CHUNKS: usize = 8;
const CONCURRENT_FILES: usize = 4;
const CHUNK_SIZE: u64 = 1024 * 1024 * 50;

pub struct FsspecStore {
    store: Arc<DynMultiPartObjectStore>,
}

impl FsspecStore {
    pub fn new(store: Arc<DynMultiPartObjectStore>) -> Self {
        Self { store }
    }
    async fn put_file(&self, lpath: &str, rpath: &str) -> Result<()> {
        let key = Path::from(rpath);
        let file_size = fs::metadata(lpath)?.len();

        // if the file is less than 100MB, use the single-part upload
        if file_size < cmp::min(5 * 2u64.pow(30), 1024 * 1024 * 100) {
            let file_content = fs::read(lpath)?;
            self.store.put(&key, file_content.into()).await?;
        } else {
            let mut chunk_count = (file_size / CHUNK_SIZE) + 1;
            let mut size_of_last_chunk = file_size % CHUNK_SIZE;
            if size_of_last_chunk == 0 {
                size_of_last_chunk = CHUNK_SIZE;
                chunk_count -= 1;
            }
            let upload_id = self.store.create_multipart(&key).await?;
            let upload_futures: Vec<_> = (0..chunk_count)
                .map(|chunk_index| {
                    let key = &key;
                    let lpath = &lpath;
                    let upload_id = &upload_id;
                    let store = &self.store;
                    async move {
                        let this_chunk = if chunk_count - 1 == chunk_index {
                            size_of_last_chunk
                        } else {
                            CHUNK_SIZE
                        };
                        let start_byte = chunk_index * CHUNK_SIZE;
                        let mut file = tokio::fs::OpenOptions::new()
                            .read(true)
                            .open(&lpath)
                            .await
                            .expect("Unable to open file");
                        file.seek(SeekFrom::Start(start_byte))
                            .await
                            .expect("Failed to seek in file");
                        let mut buffer = vec![0; this_chunk as usize];
                        file.read_exact(&mut buffer)
                            .await
                            .expect("Failed to read chunk from file");
                        store
                            .put_part(key, upload_id, chunk_index as usize, buffer.into())
                            .await
                            .expect("Failed to upload part")
                    }
                })
                .collect();

            // create a buffered stream that will execute up to 8 futures in parallel
            let stream = futures::stream::iter(upload_futures).buffered(CONCURRENT_CHUNKS);
            // wait for all futures to complete
            let parts = stream.collect::<Vec<_>>().await;
            self.store
                .complete_multipart(&key, &upload_id, parts)
                .await?;
        }
        Ok(())
    }

    async fn get_file(&self, rpath: &str, lpath: &str) -> Result<()> {
        let key = Path::from(rpath);
        // delete the file if it exists
        let _ = fs::remove_file(lpath);
        // create parent directories if they don't exist
        if let Some(parent) = StdPath::new(lpath).parent() {
            fs::create_dir_all(parent)?;
        }
        let file_size = self.store.head(&key).await?.size as u64;
        let mut chunk_count = file_size / CHUNK_SIZE;
        if file_size % CHUNK_SIZE > 0 {
            chunk_count += 1;
        }
        let download_futures: Vec<_> = (0..chunk_count)
            .map(|chunk_index| {
                let key = &key;
                let lpath = &lpath;
                let store = &self.store;
                async move {
                    let start_byte = chunk_index * CHUNK_SIZE;
                    let end_byte = std::cmp::min(start_byte + CHUNK_SIZE, file_size);
                    let downloaded_bytes = store
                        .get_range(
                            key,
                            std::ops::Range {
                                start: start_byte as usize,
                                end: end_byte as usize,
                            },
                        )
                        .await?;
                    // Open the file and seek to the appropriate position
                    let mut file = tokio::fs::OpenOptions::new()
                        .write(true)
                        .create(true)
                        .truncate(false)
                        .open(&lpath)
                        .await?;
                    file.seek(SeekFrom::Start(start_byte)).await?;
                    file.write_all(&downloaded_bytes).await?;
                    Ok::<(), Box<dyn std::error::Error>>(())
                }
            })
            .collect();
        // create a buffered stream that will execute up to 8 futures in parallel
        let stream = futures::stream::iter(download_futures).buffer_unordered(CONCURRENT_CHUNKS);
        // wait for all futures to complete
        stream.collect::<Vec<_>>().await;
        Ok(())
    }

    // recursively get all local paths
    fn get_local_paths(path: &StdPath) -> Result<Vec<String>> {
        let mut files = Vec::new();
        if path.is_dir() {
            for entry in fs::read_dir(path)? {
                let entry = entry?;
                let path = entry.path();
                if path.is_dir() {
                    files.extend(Self::get_local_paths(&path)?);
                } else if let Some(path_str) = path.to_str() {
                    files.push(path_str.to_string());
                }
            }
        } else if let Some(path_str) = path.to_str() {
            files.push(path_str.to_string());
        }
        Ok(files)
    }
}

impl Fsspec for FsspecStore {
    async fn info(&self, path: &str) -> Result<Details> {
        let mut info: Details = HashMap::new();
        let mut obj_type = "file";
        let mut size = 0;

        if self.is_dir(path).await? {
            obj_type = "directory";
        } else {
            size = self.store.head(&Path::from(path)).await?.size;
        };
        info.insert("name".to_string(), Info::Name(path.to_string()));
        info.insert("size".to_string(), Info::Size(size));
        info.insert("type".to_string(), Info::Type(obj_type.to_string()));
        Ok(info)
    }

    async fn get(&self, rpath: &str, lpath: &str, recursive: bool) -> Result<()> {
        let std_lpath = StdPath::new(lpath);
        if recursive {
            let rpaths = self.ls(rpath, false).await?;
            let get_file_futures: Vec<_> = rpaths
                .iter()
                .map(|cur_rpath| async move {
                    let cur_rpath = match cur_rpath {
                        ListInfo::Location(cur_rpath) => cur_rpath,
                        _ => panic!("rpath is not a location"),
                    };
                    let file_name = cur_rpath
                        .strip_prefix(rpath)
                        .unwrap()
                        .trim_start_matches('/');
                    if file_name.is_empty() {
                        return Ok(());
                    }
                    let lpath = std_lpath.join(file_name);
                    self.get_file(cur_rpath, lpath.to_str().unwrap()).await
                })
                .collect();
            let stream = futures::stream::iter(get_file_futures).buffer_unordered(CONCURRENT_FILES);
            // wait for all futures to complete
            stream.collect::<Vec<_>>().await;
        } else {
            // if lpath ends with a "/", append rpath's file name to it
            let mut lpath = lpath.to_string();
            if lpath.ends_with('/') {
                lpath = format!("{}{}", lpath, rpath.rsplit('/').next().unwrap_or(""));
            }
            self.get_file(rpath, lpath.as_str()).await?;
        }
        Ok(())
    }

    async fn put(&self, lpath: &str, rpath: &str, recursive: bool) -> Result<()> {
        let std_lpath = StdPath::new(lpath);
        let std_rpath = StdPath::new(rpath);
        if recursive {
            let lpaths = Self::get_local_paths(std_lpath)?;
            let put_file_futures: Vec<_> = lpaths
                .iter()
                .map(|cur_lpath| async move {
                    let file_name = cur_lpath
                        .strip_prefix(lpath)
                        .unwrap()
                        .trim_start_matches('/');
                    let rpath = if lpath.ends_with('/') {
                        std_rpath.join(file_name)
                    } else {
                        let dir = lpath.split('/').last().unwrap();
                        std_rpath.join(dir).join(file_name)
                    };
                    self.put_file(cur_lpath, rpath.to_str().unwrap()).await
                })
                .collect();
            let stream = futures::stream::iter(put_file_futures).buffer_unordered(CONCURRENT_FILES);
            stream.collect::<Vec<_>>().await;
        } else {
            if std_lpath.is_dir() {
                return Err(anyhow::anyhow!(
                    "If recursive=false, lpath should not be a directory"
                ));
            }
            self.put_file(lpath, rpath).await?;
        }
        Ok(())
    }

    async fn ls(&self, path: &str, detail: bool) -> Result<Vec<ListInfo>> {
        let path = Path::from(path);
        let list = {
            let list = self.store.list_with_delimiter(Some(&path)).await?;
            match detail {
                true => list
                    .common_prefixes
                    .iter()
                    .map(|item| {
                        ListInfo::Details(FileInfo {
                            metadata: None,
                            location: item.to_string(),
                            file_type: "directory".to_string(),
                        })
                    })
                    .chain(list.objects.iter().map(|item| {
                        ListInfo::Details(FileInfo {
                            metadata: Some(item.clone()),
                            location: item.location.to_string(),
                            file_type: "file".to_string(),
                        })
                    }))
                    .collect(),
                false => list
                    .common_prefixes
                    .iter()
                    .map(|item| ListInfo::Location(item.to_string()))
                    .chain(
                        list.objects
                            .iter()
                            .map(|item| ListInfo::Location(item.location.to_string())),
                    )
                    .collect(),
            }
        };
        Ok(list)
    }

    async fn is_dir(&self, path: &str) -> Result<bool> {
        let list = self.ls(path, false).await?;
        Ok(!list.is_empty())
    }

    fn open(&self, path: &str, mode: &str) -> Result<FileHandle> {
        Ok(FileHandle::new(Path::from(path), self.store.clone(), mode))
    }
}
