from contextlib import contextmanager
from time import perf_counter
import os
from typing import Any
from pathlib import Path
import sys
from subprocess import run, Popen, PIPE

from rich import print
from rich.progress import track

NUITKA_VERSIONS = ["nuitka", '"https://github.com/Nuitka/Nuitka/archive/factory.zip"']


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
    if is_in_venv():
        return resolved_path
    else:
        venv_create = run(f"{resolved_path} -m venv venv", stdout=PIPE, stderr=PIPE)
        if venv_create.returncode != 0:
            raise RuntimeError("Failed to create venv")

        new_venv_path = Path("venv")
        if new_venv_path.exists():
            return (new_venv_path / "Scripts" / "python.exe").resolve()
        else:
            raise FileNotFoundError("Failed to create venv")


def create_venv_with_version(version: str) -> Path:
    venv_create = run(f"py -{version} -m venv {version}_venv")
    if venv_create.returncode != 0:
        raise RuntimeError("Failed to create venv")

    new_venv_path = Path(f"{version}_venv")
    if new_venv_path.exists():
        return (new_venv_path / "Scripts" / "python.exe").resolve()
    else:
        raise FileNotFoundError("Failed to create venv")


def run_benchmark(
    benchmark: Path,
    python_executable: Path,
    iterations: int,
    cpython_version: str,
    nuitka_version: str,
    type: str,
    nuitka_name: str,
) -> dict[str, list[float]]:
    local_results: dict[str, list[float]] = {
        "warmup": [],
        "benchmark": [],
    }
    run_command = {
        "Nuitka": Path(os.getcwd()) / "run_benchmark.dist/run_benchmark.exe",
        "CPython": [python_executable, "run_benchmark.py"],
    }

    for _ in track(
        list(range(iterations)),
        description=f"Running benchmark {benchmark.name} with {nuitka_name} | Python Version: {cpython_version}-warmup",
    ):
        with Timer() as timer:
            res = run(run_command[type])  # type: ignore
            if res.returncode != 0:
                raise RuntimeError(f"Failed to run benchmark {benchmark.name}")
        local_results["warmup"].append(timer.time_taken)

    for _ in track(
        list(range(iterations)),
        description=f"Running benchmark {benchmark.name} with {nuitka_name} | Python Version: {cpython_version}-benchmark",
    ):
        with Timer() as timer:
            res = run(run_command[type])  # type: ignore
            if res.returncode != 0:
                raise RuntimeError(f"Failed to run benchmark {benchmark.name}")

        local_results["benchmark"].append(timer.time_taken)

    # print(f"Ran benchmark {benchmark.name} with {nuitka_version} | pyver {cpython_version}")
    print(f"Ran benchmark {benchmark.name} with {nuitka_name} | Python Version: {cpython_version}")

    return local_results


def parse_py_launcher():
    BLACKLIST = ["3.13", "3.13t"]
    res = Popen(["py", "-0"], shell=True, stdout=PIPE, stderr=PIPE)
    resp = [line.decode("utf-8").strip().split("Python") for line in res.stdout]
    if "Active venv" in resp[0][0]:
        resp.pop(0)
    versions = [
        version[0].strip().replace("-V:", "").replace(" *", "") for version in resp
    ]
    versions = [version for version in versions if version not in BLACKLIST]
    return versions


def is_in_venv():
    # https://stackoverflow.com/a/1883251
    return sys.prefix != sys.base_prefix
