import abc
import pandas as pd
import vaex as vx
import pyarrow as pa
import pyarrow.parquet as pq
import io
from typing import Dict, List, Union, Any
import json
from .filesystem import FileSystem
from .filesystem import LocalBackend, DropboxBackend
from .rdb import RDB


class Storage:
    """
    A python object storage with various backend assigned.
    """

    def __init__(self, backend: FileSystem):
        """
        Args:
            backend (Backend): A remote storage backend
            to be use for the python object storage.
        """
        self._backend = backend

    def get_upload_type(self):
        first_input_arg = list(self.upload.__annotations__.keys())[0]
        return self.upload.__annotations__[first_input_arg]

    def get_download_type(self):
        return self.download.__annotations__['return']

    @abc.abstractmethod
    def upload(self, obj: Any, obj_id: str):
        """Upload of obj as a file at remote path

        Args:
            obj (object): object to be upload
            obj_id (str): path to upload
        """
        raise NotImplementedError

    @abc.abstractmethod
    def download(self, obj_id: str) -> Any:
        """Download obj from remote path
        Args:
            obj_id (str): The path to be download from.
        Returns:
            object: The downloaded file.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def check_exists(self, obj_id: str) -> bool:
        """
        Check whether an object exists
        """
        raise NotImplementedError

    @abc.abstractmethod
    def drop(self, obj_id: str):
        """
        Delete an object
        """
        raise NotImplementedError

    @abc.abstractmethod
    def copy(self, src_obj_id: str, dest_obj_id: str):
        """
        Copy an object
        """
        raise NotImplementedError


JsonType = Union[None, int, str, bool, List[Any], Dict[str, Any]]


class JsonStorage(Storage):
    """
    Storage of JSON Python Diction
    """

    def __init__(self, filesystem: FileSystem):
        assert isinstance(
            filesystem, FileSystem), 'Json Storage should have FileSystem backend'
        super().__init__(backend=filesystem)

    def upload(self, json_obj: JsonType, obj_id: str):
        """Upload a python object as json on a filesystem

        Args:
            json (Union[Dict, List]): A json parsable python object
            obj_id (str): The id of the object
        """
        buff = io.BytesIO(json.dumps(json_obj).encode())
        self._backend.upload_core(buff, obj_id + '.json')

    def download(self, obj_id: str) -> JsonType:
        buff = self._backend.download_core(obj_id + '.json')
        buff.seek(0)
        return json.loads(buff.read().decode())

    def check_exists(self, obj_id: str) -> bool:
        return self._backend.check_exists(obj_id + '.json')

    def drop(self, obj_id: str):
        return self._backend.drop_file(obj_id + '.json')

    def copy(self, src_obj_id: str, dest_obj_id: str):
        self._backend.copy_file(
            src_obj_id + '.json',
            dest_obj_id + '.json'
        )


class DataFrameStorage(Storage):
    """
    Storage of DataFrame
    """

    def __init__(self, backend: FileSystem):
        super().__init__(backend=backend)

    @abc.abstractmethod
    def upload(self, dataframe: Union[pd.DataFrame,
               vx.DataFrame, pa.Table], obj_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def download(
            self, obj_id: str) -> Union[pd.DataFrame, vx.DataFrame, pa.Table]:
        raise NotImplementedError

    def check_exists(self, obj_id: str) -> bool:
        return self._backend.check_exists(obj_id + '.parquet')

    def drop(self, obj_id: str):
        return self._backend.drop_file(obj_id + '.parquet')

    def copy(self, src_obj_id: str, dest_obj_id: str):
        self._backend.copy_file(
            src_obj_id + '.parquet',
            dest_obj_id + '.parquet'
        )


class PandasStorage(DataFrameStorage):
    """
    Storage of Pandas DataFrame
    """

    def upload(self, dataframe: pd.DataFrame, obj_id: str):
        if isinstance(self._backend, FileSystem):
            buff = io.BytesIO()
            dataframe.to_parquet(buff)
            self._backend.upload_core(buff, obj_id + '.parquet')
        elif isinstance(self._backend, RDB):
            cursor = self._backend.get_conn()
            try:
                cursor.register(obj_id, dataframe)
            finally:
                cursor.close()
        else:
            raise TypeError(
                f'backend should be FileSystem/RDB, but it is {self._backend}')

    def download(self, obj_id: str) -> pd.DataFrame:
        if isinstance(self._backend, FileSystem):
            buff = self._backend.download_core(obj_id + '.parquet')
            result = pd.read_parquet(buff, engine='pyarrow')
            return result
        elif isinstance(self._backend, RDB):
            cursor = self._backend.get_conn()
            try:
                return cursor.execute(f'SELECT * FROM {obj_id};').df()
            finally:
                cursor.close()
        else:
            raise TypeError(
                f'backend should be FileSystem, but it is {self._backend}')


class PyArrowStorage(DataFrameStorage):
    """Storage of pyarrow Table
    """

    def upload(self, dataframe: pa.Table, obj_id: str):
        if isinstance(self._backend, FileSystem):
            buff = io.BytesIO()
            pq.write_table(dataframe, buff)
            self._backend.upload_core(buff, obj_id + '.parquet')
        elif isinstance(self._backend, RDB):
            cursor = self._backend.get_conn()
            try:
                cursor.register(obj_id, dataframe)
            finally:
                cursor.close()
        else:
            raise TypeError(
                f'backend should be FileSystem, but it is {self._backend}')

    def download(self, obj_id: str) -> pa.Table:
        if isinstance(self._backend, FileSystem):
            buff = self._backend.download_core(obj_id + '.parquet')
            return pq.read_table(buff)
        elif isinstance(self._backend, RDB):
            cursor = self._backend.get_conn()
            try:
                return cursor.execute(f'SELECT * FROM {obj_id};').arrow()
            finally:
                cursor.close()
        else:
            raise TypeError(
                f'backend should be FileSystem, but it is {self._backend}')


class VaexStorage(DataFrameStorage):
    """Storage of Vaex DataFrame
    """

    def upload(self, dataframe: vx.DataFrame, obj_id: str):
        if isinstance(self._backend, FileSystem):
            # Try using multithread + io.pipe to stream vaex
            # to target directory
            buff = io.BytesIO()
            dataframe.export_parquet(buff)
            self._backend.upload_core(buff, obj_id + '.parquet')
        else:
            raise TypeError('backend should be FileSystem')

    def download(self, obj_id: str) -> vx.DataFrame:
        if isinstance(self._backend, LocalBackend):
            path = self._backend._fs.path
            # if path.startswith('/'):
            #     path = path[1:]
            result = vx.open(
                f'{path}/{obj_id}' +
                '.parquet')
            return result
        elif isinstance(self._backend, DropboxBackend):
            buff = self._backend.download_core(obj_id + '.parquet')
            buff.seek(0)
            path = self._backend._fs.path
            if path.startswith('/'):
                path = path[1:]
            lfs = LocalBackend(path)
            lfs.upload_core(buff, remote_path=obj_id + '.parquet')
            result = vx.open(
                f'{path}/{obj_id}' +
                '.parquet')
            return result
        else:
            raise TypeError('backend should be FileSystem')
