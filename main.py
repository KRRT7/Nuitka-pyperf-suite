from Utilities import temporary_directory_change, resolve_venv_path, run_benchmark
from pathlib import Path
import shutil
from subprocess import run
from rich import print

BENCHMARK_DIRECTORY = Path("benchmarks")


for benchmark in BENCHMARK_DIRECTORY.iterdir():
    if benchmark.is_dir() and not benchmark.name.startswith("bm_"):
        continue

    if benchmark.is_dir():
        orig_path = benchmark.resolve()
        bench_results: dict[str, list[float]] = {
            "nuitka": [],
            "cpython": [],
        }
        with temporary_directory_change(benchmark):
            requirements_exists = (orig_path / "requirements.txt").exists()
            if not (orig_path / "run_benchmark.py").exists():
                print(
                    f"Skipping benchmark {benchmark.name}, because {orig_path / 'run_benchmark.py'} does not exist"
                )
                continue

            python_executable = resolve_venv_path()
            print(f"Using python executable {python_executable}")

            commands = [
                f"{python_executable} --version",
                f"{python_executable} -m pip install nuitka pyperf",
                f"{python_executable} -m nuitka --standalone --remove-output run_benchmark.py",
            ]
            if requirements_exists:
                commands.insert(
                    2, f"{python_executable} -m pip install -r requirements.txt"
                )

            for command in commands:
                print(f"Running command {command}")
                res = run(command)
                if res.returncode != 0:
                    print(f"Failed to run command {command}")
                    break

            bench_results["nuitka"] = run_benchmark(
                benchmark, python_executable, 50, "nuitka", "Nuitka"
            )
            bench_results["cpython"] = run_benchmark(
                benchmark, python_executable, 50, "cpython", "CPython"
            )
            print(bench_results)
        # cleanup the benchmark directory venv
        venv_path = python_executable.parent.parent

        # print(f"Removing venv {venv_path}")
        shutil.rmtree(venv_path)
        shutil.rmtree(benchmark / "run_benchmark.dist")
