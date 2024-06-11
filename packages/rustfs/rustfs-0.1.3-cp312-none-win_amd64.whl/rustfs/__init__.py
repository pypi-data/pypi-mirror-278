import fsspec
from .core import RustFileSystem


print("init rustfs")
fsspec.register_implementation(name="s3", cls=RustFileSystem, clobber=True)
