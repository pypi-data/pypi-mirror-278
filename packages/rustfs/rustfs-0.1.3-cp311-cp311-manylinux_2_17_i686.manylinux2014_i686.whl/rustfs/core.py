from fsspec.asyn import AbstractFileSystem
from .rustfs import RustFileSystem as _RustFileSystem

import logging

logger = logging.getLogger(__name__)


class RustFileSystem(AbstractFileSystem):
    def __init__(self, **kwargs):
        logger.info("Initializing RustFileSystem")
        super().__init__(**kwargs)
        self._fs = _RustFileSystem(**kwargs)

    def put(
        self,
        lpath,
        rpath,
        **kwargs,
    ):
        return self._fs.put(lpath, rpath, **kwargs)

    def get(
        self,
        rpath,
        lpath,
        **kwargs,
    ):
        return self._fs.get(rpath, lpath, **kwargs)

    def open(
        self,
        path,
        mode="rb",
        **kwargs,
    ):
        return self._fs.open(path, mode, **kwargs)

    def info(self, path, **kwargs):
        return self._fs.info(path, **kwargs)

    def ls(self, path, detail=False, **kwargs):
        return self._fs.ls(path, detail=detail, **kwargs)
