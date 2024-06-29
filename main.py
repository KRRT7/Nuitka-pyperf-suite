from Utilities import (
    temporary_directory_change,
    run_benchmark,
    parse_py_launcher,
    create_venv_with_version,
    get_benchmark_setup,
    setup_benchmark_enviroment,
    Benchmark,
    Stats,
)
import platform
import shutil
from subprocess import run, PIPE
from rich import print
import json
from datetime import datetime
from itertools import product

ITERATIONS = 100

if platform.system() == "Windows":

    versions = parse_py_launcher()

    for python_version, nuitka_version in product(
        versions,
        ["nuitka", '"https://github.com/Nuitka/Nuitka/archive/factory.zip"'],
    ):
        nuitka_name = (
            "Nuitka-stable" if "github" not in nuitka_version else "Nuitka-factory"
        )
        benchmarks = get_benchmark_setup()
        for benchmark in benchmarks:
            orig_path = benchmark.resolve()

            results_dir = orig_path / "results" / datetime.now().strftime("%Y-%m-%d")
            results_file = results_dir / f"{nuitka_name}-{python_version}.json"

            if results_file.exists() and results_file.stat().st_size > 0:
                print(
                    f"Skipping benchmark {benchmark.name}, because results exist for {benchmark.name} with {python_version} and {nuitka_name}"
                )
                continue

            if not results_dir.exists():
                results_dir.mkdir(parents=True, exist_ok=True)
            results_file.touch(exist_ok=True)

            bench_result = Benchmark(
                target=nuitka_name,
                nuitka_version=nuitka_version,
                python_version=Benchmark.parse_file_name(results_file.stem)[2],
                benchmark_name=benchmark.name,
            )

            with temporary_directory_change(benchmark):
                requirements_exists = (orig_path / "requirements.txt").exists()
                if not (orig_path / "run_benchmark.py").exists():
                    print(
                        f"Skipping benchmark {benchmark.name}, because {orig_path / 'run_benchmark.py'} does not exist"
                    )
                    continue

                python_executable = create_venv_with_version(python_version)
                setup_benchmark_enviroment(
                    nuitka_version,
                    requirements_exists,
                    str(python_executable.resolve()),
                    silent=False,
                    compilation_type="accelerated",
                )
            
                try:
                    nuitka_benchmark = run_benchmark(
                        benchmark,
                        python_executable,
                        ITERATIONS,
                        python_version,
                        "Nuitka",
                        nuitka_name,
                        "accelerated",
                    )

                    bench_result.nuitka_stats = Stats.from_dict(
                        nuitka_benchmark, "nuitka"
                    )

                    cpython_benchmark = run_benchmark(
                        benchmark,
                        python_executable,
                        ITERATIONS,
                        python_version,
                        "CPython",
                        nuitka_name,
                        "accelerated",
                    )

                    bench_result.cpython_stats = Stats.from_dict(
                        cpython_benchmark, "cpython"
                    )

                    bench_result.to_json_file(results_file)

                except KeyboardInterrupt:
                    print(
                        f"Interrupted running benchmark {benchmark.name} with {python_version}, cleaning up"
                    )
                    raise SystemExit from None
                except Exception as e:
                    print(
                        f"Failed to run benchmark {benchmark.name} with {python_version}\n{e}"
                    )
                    break
                finally:
                    # cleanup the benchmark directory venv and dist
                    venv_path = python_executable.parent.parent
                    dist_path = (orig_path / "run_benchmark.dist").resolve()

                    shutil.rmtree(venv_path)
                    if dist_path.exists():
                        shutil.rmtree(dist_path)
