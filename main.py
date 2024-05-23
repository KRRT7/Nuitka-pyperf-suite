from Utilities import Timer, temporary_directory_change, resolve_venv_path
import os
from rich import print
from pathlib import Path
from subprocess import run
from shlex import split


BENCHMARK_DIRECTORY = Path("benchmarks")

for benchmark in BENCHMARK_DIRECTORY.iterdir():
    if benchmark.is_dir() and not benchmark.name.startswith("bm_"):
        continue

    if benchmark.is_dir():
        print(f"Running benchmark {benchmark.name}")
        with temporary_directory_change(benchmark):
            # commands = [
            #     "python -m venv venv",
            #     "venv\\Scripts\\activate",
            #     "python --version",
            #     "pip install nuitka",
            # ]
            commands = [
                f"{resolve_venv_path()} --version",
                f"{resolve_venv_path()} -m pip install nuitka pyperf",
                f"{resolve_venv_path()} -m nuitka --onefile --remove-output run_benchmark.py",
                f"run_benchmark.exe",
            ]
            for command in commands:
                print(f"Running command {command}")
                res = run(command)
                if res.returncode != 0:
                    print(f"Failed to run command {command}")
                    break
