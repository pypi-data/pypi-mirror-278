import platform
from abc import ABC, abstractmethod
from typing import Any, Type
import json
import os
from pathlib import Path


class FunctionClass(ABC):
    def __new__(cls, *args, **kwargs) -> Any:
        instance = super().__new__(cls)
        return instance(*args, **kwargs)

    @abstractmethod
    def __call__(self, *args, **kwargs): ...


class is_sys(FunctionClass):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MACOS = 'Darwin'

    def __new__(cls, os_name: str) -> bool:
        return super().__new__(cls, os_name)

    def __call__(self, os_name: str) -> bool:
        this_os_name = platform.system()
        if os_name == this_os_name:
            return True
        return False


def recursive_convert(data: list | tuple, to: Type) -> tuple | list:
    """Recursively convert the lists and tuples are nested within each other to only tuples or lists"""
    if isinstance(data, (list, tuple)):
        return to(recursive_convert(item, to=to) for item in data)
    return data


class get_env(FunctionClass):
    ENV_FILE = '.env'

    @staticmethod
    def _parse_key_value() -> dict:
        result = {}
        lines = Path(get_env.ENV_FILE).read_text(encoding='utf-8').strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                key_value = line.split('=', maxsplit=2)
                result[key_value[0].strip()] = key_value[1].strip()
        return result

    def __new__(cls, env_name: str) -> Any:
        return super().__new__(cls, env_name)

    def __call__(self, env_name: str) -> Any:
        env = os.environ.get(env_name)
        try:
            return json.loads(env)
        except json.decoder.JSONDecodeError:
            return env
        except TypeError:
            for key_value in self._parse_key_value().items():
                os.environ[key_value[0]] = key_value[1]
            return get_env(env_name)
