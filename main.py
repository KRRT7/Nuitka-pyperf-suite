from Utilities import (
    temporary_directory_change,
    run_benchmark,
    parse_py_launcher,
    create_venv_with_version,
    NUITKA_VERSIONS,
)
from pathlib import Path
import shutil
from subprocess import run, PIPE
from rich import print
from rich.table import Table
from itertools import product

BENCHMARK_DIRECTORY = Path("benchmarks")
ITERATIONS = 100


versions = parse_py_launcher()

for python_version, nuitka_version in product(versions, NUITKA_VERSIONS):
    for benchmark in BENCHMARK_DIRECTORY.iterdir():
        if benchmark.is_dir() and not benchmark.name.startswith("bm_"):
            continue

        if benchmark.is_dir():
            orig_path = benchmark.resolve()
            bench_results: dict[str, dict[str, list[float]]] = {
                "nuitka": {"benchmark": [], "warmup": []},
                "cpython": {"benchmark": [], "warmup": []},
            }

            with temporary_directory_change(benchmark):
                requirements_exists = (orig_path / "requirements.txt").exists()
                if not (orig_path / "run_benchmark.py").exists():
                    print(
                        f"Skipping benchmark {benchmark.name}, because {orig_path / 'run_benchmark.py'} does not exist"
                    )
                    continue
                python_executable = create_venv_with_version(python_version)
                try:
                    commands = [
                        f"{python_executable} --version",
                        f"{python_executable} -m pip install --upgrade pip",
                        f"{python_executable} -m pip install {nuitka_version}",
                        f"{python_executable} -m nuitka --standalone --remove-output run_benchmark.py",
                    ]
                    if requirements_exists:
                        commands.insert(
                            2, f"{python_executable} -m pip install -r requirements.txt"
                        )

                    for command in commands:
                        res = run(command, stdout=PIPE, stderr=PIPE)
                        if res.returncode != 0:
                            print(f"Failed to run command {command}")
                            break

                    bench_results["nuitka"] = run_benchmark(
                        benchmark,
                        python_executable,
                        ITERATIONS,
                        python_version,
                        nuitka_version,
                    )

                    bench_results["cpython"] = run_benchmark(
                        benchmark,
                        python_executable,
                        ITERATIONS,
                        python_version,
                        nuitka_version,
                    )

                    results = Table(
                        title=f"Benchmarks for {benchmark.name}, {python_version}"
                    )
                    results.add_column("Benchmark", justify="left", style="cyan")
                    results.add_column("Nuitka", justify="right", style="magenta")
                    results.add_column("CPython", justify="right", style="green")

                    for key in ["warmup", "benchmark"]:
                        results.add_row(
                            key,
                            f"{sum(bench_results['nuitka'][key]) / ITERATIONS:.2f}",
                            f"{sum(bench_results['cpython'][key]) / ITERATIONS:.2f}",
                        )

                    min_nuitka = min(
                        sum(bench_results["nuitka"]["benchmark"]) / ITERATIONS,
                        sum(bench_results["nuitka"]["warmup"]) / ITERATIONS,
                    )

                    min_cpython = min(
                        sum(bench_results["cpython"]["benchmark"]) / ITERATIONS,
                        sum(bench_results["cpython"]["warmup"]) / ITERATIONS,
                    )
                    if min_nuitka < min_cpython:
                        print(
                            f"{nuitka_version} is faster for benchmark {benchmark.name} by {(min_cpython - min_nuitka):.2f}"
                        )
                    else:
                        print(
                            f"{python_version} is faster for benchmark {benchmark.name} by {(min_nuitka - min_cpython):.2f}"
                        )

                    # cleanup the benchmark directory venv
                except KeyboardInterrupt:
                    print(
                        f"Interrupted running benchmark {benchmark.name} with {python_version}, cleaning up"
                    )
                    break
                except Exception as e:
                    print(
                        f"Failed to run benchmark {benchmark.name} with {python_version}"
                    )
                    print(e)
                    break
                finally:
                    # cleanup the benchmark directory venv and dist
                    venv_path = python_executable.parent.parent
                    dist_path = benchmark / "run_benchmark.dist"
                    # print(f"Removing venv {venv_path}")
                    shutil.rmtree(venv_path)
                    if dist_path.exists():
                        shutil.rmtree(dist_path)
