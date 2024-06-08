import functools
import re
from pathlib import Path
from typing import Callable


def _path_operation(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(path: str | Path) -> str | Path:
        original_type = type(path)
        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise ValueError(f"Path must be a string or Path object, not {original_type}")

        new_path = func(path)

        if original_type is str:
            return str(new_path)
        return new_path

    return wrapper


@_path_operation
def auto_rename(path: str | Path) -> str | Path:
    """If the file name has existed, add (n) after the file name and return, or return the original name."""
    n = 0
    while path.exists():
        n += 1
        stem = re.sub(r"\(\d+\)$", "", path.stem)
        path = path.with_name(f'{stem}({n}){path.suffix}')
    return path
