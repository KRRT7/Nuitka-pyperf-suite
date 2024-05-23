from contextlib import contextmanager
from time import perf_counter
import os
from typing import Any
from pathlib import Path


class Timer:
    def __init__(self):
        self.start = 0
        self.end = 0

        self.time_taken = 0

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = perf_counter()

        self.time_taken = self.end - self.start

    def __call__(self, func: Any):
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper


@contextmanager
def temporary_directory_change(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Directory {path} does not exist")
    current_directory = Path.cwd()
    os.chdir(path)
    yield
    os.chdir(current_directory)


def resolve_venv_path() -> Path:
    venv_path = Path("venv")

    if venv_path.exists():
        return (venv_path / "Scripts" / "python.exe").resolve()
    else:
        raise FileNotFoundError("venv directory not found")
