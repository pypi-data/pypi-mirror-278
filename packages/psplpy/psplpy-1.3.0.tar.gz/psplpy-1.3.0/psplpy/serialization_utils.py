import base64
import io
import json
import lzma
import pickle
import yaml
import re
import zlib
from pathlib import Path
from types import ModuleType
from typing import Any


class Compressor:
    LZMA = lzma
    ZLIB = zlib

    def __init__(self, lib: ModuleType = LZMA, encoding: str = 'utf-8'):
        self.lib = lib
        self.encoding = encoding

    def compress(self, data: bytes) -> bytes:
        compressed_data = self.lib.compress(data)
        return compressed_data

    def decompress(self, compressed_data: bytes) -> bytes:
        data = self.lib.decompress(compressed_data)
        return data


class _DataInFile:
    _MARK = b'"""'
    _UNIQUE_MARK = b'2qIgKf9iDsVrsTMS'
    _PRE_MARK = _MARK + _UNIQUE_MARK
    _POST_MARK = _UNIQUE_MARK + _MARK
    _WIN_ESP = b'\r\n'

    def find_start_and_end_index(self, data: bytes) -> tuple[int, int]:
        start_index = data.find(self._PRE_MARK)
        end_index = data.find(self._POST_MARK)
        if start_index != -1 and end_index != -1:
            start_index = start_index + len(self._PRE_MARK)

            pre_esp = data[start_index: start_index + len(self._WIN_ESP)]
            post_esp = data[end_index - len(self._WIN_ESP): end_index]
            if pre_esp == self._WIN_ESP:
                start_index += len(self._WIN_ESP)
            else:
                start_index += 1
            if post_esp == self._WIN_ESP:
                end_index -= len(self._WIN_ESP)
            else:
                end_index -= 1
            return start_index, end_index
        return -1, -1

    def get_data(self, data: bytes) -> bytes:
        start_index, end_index = self.find_start_and_end_index(data)
        if start_index != -1:
            return data[start_index: end_index]
        return b''

    def replace_data(self, original_data: bytes, data: bytes) -> bytes:
        start_index, end_index = self.find_start_and_end_index(original_data)
        if start_index != -1:
            replaced_data = original_data[:start_index] + data + original_data[end_index:]
        else:
            replaced_data = (original_data + b'\n' + self._PRE_MARK + b'\n' + data + b'\n' + self._POST_MARK + b'\n')
        return replaced_data


class Serializer:

    def __init__(self, path: str | Path = None, encoding: str = 'utf-8', data_type: type = None,
                 embedded: bool = False):
        self.path = path
        self.encoding = encoding
        self.data_type = data_type
        self.embedded = embedded
        if self.embedded:
            self._data_in_file = _DataInFile()
        self.compressor = Compressor()

    @staticmethod
    def _check_int_or_float(input_str: str) -> type:
        int_pattern = r'^[-+]?\d+$'
        float_pattern = r'^[-+]?\d+(\.\d+)?$'

        if re.match(int_pattern, input_str):
            return int
        elif re.match(float_pattern, input_str):
            return float
        else:
            return str

    def _convert_json_dict_key_to_number(self, data: Any) -> Any:
        if isinstance(data, dict):
            # if data type is dict, convert it
            converted_dict = {}
            for key, value in data.items():
                if type(key) == str:
                    trans_type = self._check_int_or_float(key)
                    key = trans_type(key)
                # process the values in dict, using recursion
                value = self._convert_json_dict_key_to_number(value)
                converted_dict[key] = value
            return converted_dict
        elif isinstance(data, (list, tuple, set)):
            # if date type is list, tuple or set, process it recursively
            converted_list = []
            for item in data:
                converted_item = self._convert_json_dict_key_to_number(item)
                converted_list.append(converted_item)
            return type(data)(converted_list)
        else:
            # if it's other type, don't process
            return data

    @staticmethod
    def _get_empty_data_structure(data_type: type | None) -> dict | list | tuple | set | None:
        if data_type is None:
            return None
        types = (dict, list, tuple, set)
        if data_type in types:
            return data_type()
        else:
            raise TypeError(f"Unsupported data type {data_type}")

    def _load(self, lib: ModuleType, data: str | bytes = None, decompress: bool = False, from_b64: bool = False) -> Any:
        if not data:
            try:
                data = Path(self.path).read_bytes()
            except FileNotFoundError:  # when file not found
                return self._get_empty_data_structure(self.data_type)
        if self.embedded:
            data = self._data_in_file.get_data(data)
            # embed pickle data in file need to transform to string to avoid potential errors
            if lib is pickle and not from_b64:
                data = base64.b64decode(data.decode())
        if from_b64:
            data = base64.b64decode(data.decode())
        if decompress:
            data = self.compressor.decompress(data)

        if lib in [json, yaml]:
            if isinstance(data, bytes):
                data = data.decode(self.encoding)
            if lib is json:
                try:
                    deserialized_data = json.loads(data)
                except json.decoder.JSONDecodeError:  # when file is empty
                    return self._get_empty_data_structure(self.data_type)
            elif lib is yaml:
                deserialized_data = yaml.safe_load(data)
        elif lib is pickle:
            try:
                deserialized_data = pickle.loads(data)
            except EOFError:  # when file is empty
                return self._get_empty_data_structure(self.data_type)
        else:
            raise AssertionError
        return deserialized_data

    def _postprocess_loaded_json(self, json_data: Any, trans_key_to_num: bool = False) -> Any:
        if trans_key_to_num:
            json_data = self._convert_json_dict_key_to_number(json_data)
        if json_data is None:  # when value is null
            return self._get_empty_data_structure(self.data_type)
        return json_data

    def load_yaml(self, data: bytes = None, decompress: bool = False) -> Any:
        return self._load(yaml, data=data, decompress=decompress)

    def load_json(self, data: str | bytes = None, decompress: bool = False, trans_key_to_num: bool = False) -> Any:
        json_data = self._load(json, data=data, decompress=decompress)
        return self._postprocess_loaded_json(json_data, trans_key_to_num)

    def load_pickle(self, data: bytes = None, decompress: bool = False, from_b64: bool = False) -> Any:
        return self._load(pickle, data=data, decompress=decompress, from_b64=from_b64)

    def _dump(self, lib: ModuleType, data: bytes, compress: bool = False, to_b64: bool = False) -> bytes:
        if compress:
            data = self.compressor.compress(data)
        if to_b64:
            data = base64.b64encode(data)
        if self.embedded:
            if lib is pickle and not to_b64:
                data = base64.b64encode(data)
            original_data = Path(self.path).read_bytes()
            data = self._data_in_file.replace_data(original_data, data)
        if self.path:
            Path(self.path).write_bytes(data)
        return data

    def _get_json_dumps_data(self, data: Any, indent: int, ensure_ascii: bool, minimum: bool) -> bytes:
        if minimum:
            kwargs = {"separators": (',', ':')}
        else:
            kwargs = {"indent": indent}
        kwargs['ensure_ascii'] = ensure_ascii
        return json.dumps(data, **kwargs).encode(self.encoding)

    def dump_yaml(self, data: Any, compress: bool = False, allow_unicode: bool = True) -> bytes:
        string_io = io.StringIO()
        yaml.dump(data, string_io, allow_unicode=allow_unicode)
        data = string_io.getvalue().encode(self.encoding)
        return self._dump(yaml, data, compress=compress)

    def dump_json(self, data: Any, compress: bool = False, indent: int = 4,
                  ensure_ascii: bool = False, minimum: bool = False) -> bytes:
        data = self._get_json_dumps_data(data, indent, ensure_ascii, minimum)
        return self._dump(json, data, compress=compress)

    def dump_pickle(self, data: Any, compress: bool = False, to_b64: bool = False) -> bytes:
        data = pickle.dumps(data)
        return self._dump(pickle, data, compress=compress, to_b64=to_b64)
