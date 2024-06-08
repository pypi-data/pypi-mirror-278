import abc
import io
from fsspec import AbstractFileSystem
from ..backend import Backend


class FileSystem(Backend):
    """
    FileSystem Backend for storing python objects.

    Example: DropBoxStorage
    """

    def __init__(self, fsspec_fs: AbstractFileSystem):
        self._fs = fsspec_fs

    def upload_core(self, file_obj: io.BytesIO, remote_path: str):
        """Upload file object

        Args:
            file_obj (io.BytesIO): file to be upload
            remote_path (str): remote file path
        """
        self._upload_core(file_obj, remote_path)
        self._check_upload_success(file_obj, remote_path)
        file_obj.flush()
        file_obj.close()

    def _check_upload_success(self, file_obj: io.BytesIO, remote_path: str):
        download_data = self.download_core(remote_path)
        download_data.seek(0)
        file_obj.seek(0)
        assert download_data.getbuffer() == file_obj.getbuffer(), 'upload before != after'
        download_data.flush()
        download_data.close()

    @abc.abstractmethod
    def _upload_core(self, file_obj: io.BytesIO, remote_path: str):
        """Upload file object to local storage

        Args:
            file_obj (io.BytesIO): file to be upload
            remote_path (str): remote file path
        """
        raise NotImplementedError

    @abc.abstractmethod
    def download_core(self, remote_path: str) -> io.BytesIO:
        """Download file from remote storage

        Args:
            remote_path (str): remote file path

        Returns:
            io.BytesIO: downloaded file
        """
        raise NotImplementedError

    def check_exists(self, remote_path: str) -> bool:
        return self._fs.exists(remote_path)

    def drop_file(self, remote_path: str):
        try:
            return self._fs.rm(remote_path)
        except FileNotFoundError:
            pass

    def copy_file(self, src_file: str, dest_file):
        assert '.' in src_file, f'requires file ext .xxx provided in `src_file` but it is {src_file}'
        assert '.' in dest_file, f'requires file ext .xxx provided in `dest_file` but it is {dest_file}'
        self.drop_file(dest_file)
        self._fs.cp(src_file, dest_file, recursive=True)
