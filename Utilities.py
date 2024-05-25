from contextlib import contextmanager
from time import perf_counter
import os
from typing import Any
from pathlib import Path
import sys
from subprocess import run
from rich import print


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
    resolved_path = Path(sys.executable).resolve()
    venv_create = run(f"{resolved_path} -m venv venv")
    if venv_create.returncode != 0:
        raise RuntimeError("Failed to create venv")

    new_venv_path = Path("venv")
    if new_venv_path.exists():
        return (new_venv_path / "Scripts" / "python.exe").resolve()
    else:
        raise FileNotFoundError("Failed to create venv")


def run_benchmark(
    benchmark: Path, sys_executable: Path, iterations: int, type: str, comment: str
) -> dict[str, list[float]] | None:

    local_results: dict[str, list[float]] = {
        "warmup": [],
        "benchmark": [],
    }
    run_command = {
        "nuitka": Path(os.getcwd()) / "run_benchmark.dist/run_benchmark.exe",
        "cpython": [sys_executable, "run_benchmark.py"],
    }

    for _ in range(iterations):
        with Timer() as timer:
            res = run(run_command[type])  # type: ignore
            if res.returncode != 0:
                print(f"Failed to run benchmark {benchmark.name}")
                return None

        local_results["warmup"].append(timer.time_taken)

    for _ in range(iterations):
        with Timer() as timer:
            res = run(run_command[type])  # type: ignore
            if res.returncode != 0:
                print(f"Failed to run benchmark {benchmark.name}")
                return None

        local_results["benchmark"].append(timer.time_taken)

    print(f"Ran benchmark {benchmark.name} with {comment} {iterations} times")

    return local_results
