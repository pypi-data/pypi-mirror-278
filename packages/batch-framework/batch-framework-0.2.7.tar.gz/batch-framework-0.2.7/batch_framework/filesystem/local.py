import io
from fsspec.implementations.local import LocalFileSystem
from fsspec.implementations.dirfs import DirFileSystem
from .base import FileSystem


class LocalBackend(FileSystem):
    def __init__(self, directory='./'):
        root_fs = LocalFileSystem()
        if not root_fs.exists(directory):
            root_fs.mkdir(directory)
        super().__init__(DirFileSystem(directory))

    def _upload_core(self, file_obj: io.BytesIO, remote_path: str):
        """Upload file object to local storage

        Args:
            file_obj (io.BytesIO): file to be upload
            remote_path (str): remote file path
        """
        try:
            file_obj.seek(0)
            with self._fs.open(remote_path, 'wb') as f:
                f.write(file_obj.getbuffer())
        except BaseException as e:
            raise ValueError(f'{remote_path} upload failed') from e

    def download_core(self, remote_path: str) -> io.BytesIO:
        """Download file from remote storage

        Args:
            remote_path (str): remote file path

        Returns:
            io.BytesIO: downloaded file
        """
        try:
            with self._fs.open(remote_path, 'rb') as f:
                result = io.BytesIO(f.read())
            result.seek(0)
            return result
        except BaseException as e:
            raise ValueError(f'{remote_path} download failed') from e
