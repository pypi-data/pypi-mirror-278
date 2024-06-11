# Rust Filesystem




```python
import pandas as pd
from rustfs import RustFileSystem

df = pd.DataFrame({"name": ["Tom", "Joseph"], "age": [20, 22]})
df.to_parquet("s3://my-s3-bucket/df.parquet", storage_options={"access_key_id": "minio", "secret_access_key":"miniostorage", "endpoint": "http://localhost:30002"})


rfs = RustS3FileSystem(access_key_id="minio", secret_access_key="miniostorage", endpoint="http://localhost:30002", allow_http=True)
```


```python
from rustfs import RustFileSystem

rfs = RustFileSystem(access_key_id="minio", secret_access_key="miniostorage", endpoint="http://localhost:30002", allow_http=True)
fh = rfs.open("s3://my-s3-bucket/test.txt", "wb")

```


This is me and troy discussing things
```python
with open("s3://bucket/one_tb.file", "rb") as reader:
    with rustfs.open("s3://bucket/one_tb.copy", "wb") as writer:
        # rust writer needs to accept BinaryIO
        writer.write(reader)


with rfsopen("/local/one_tb.file", "rb") as reader:
    with rfsopen("s3://bucket/one_tb.copy", "wb") as writer:
        while True:
            b = reader.read(10)
            if not b:
                break
            writer.write(b)


with rustfs.open(""s3://bucket/one_tb.copy", "rb") as reader:
    reader.read()
```