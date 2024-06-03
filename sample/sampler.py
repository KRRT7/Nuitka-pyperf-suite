from pathlib import Path
from dataclasses import dataclass
from json import load
from rich import print
from rich.table import Table
from ..Utilities import calculate_stats


@dataclass
class Stats:
    name: str
    warmup: list[float]
    benchmark: list[float]


@dataclass
class Benchmark:
    target: str
    nuitka_version: str
    python_version: tuple[int, int]
    file_json: dict
    nuitka_stats: Stats
    cpython_stats: Stats
    benchmark_name: str

    @staticmethod
    def parse_file_name(file_name: str) -> tuple[str, str, tuple[int, int]]:
        target, nuitka_version, python_version = file_name.split("-")
        py_ver_split = python_version.split(".")
        python_version_tuple = (int(py_ver_split[0]), int(py_ver_split[1]))
        return target, nuitka_version, python_version_tuple

    @staticmethod
    def parse_stats(stats: dict) -> dict:
        nuitka_stats = stats["nuitka"]
        cpython_stats = stats["cpython"]
        return {
            "nuitka": Stats(
                "nuitka",
                nuitka_stats["warmup"],
                nuitka_stats["benchmark"],
            ),
            "cpython": Stats(
                "cpython",
                cpython_stats["warmup"],
                cpython_stats["benchmark"],
            ),
        }

    @classmethod
    def from_path(cls, file_path: Path, benchmark_name: str) -> "Benchmark":
        if not file_path.stat().st_size > 0:
            raise FileNotFoundError(f"File {file_path} does not exist or is empty")

        with open(file_path, "r") as f:
            file_json = load(f)

        file_info = cls.parse_file_name(file_path.stem)
        parsed_stats = cls.parse_stats(file_json)
        return cls(
            target=file_info[0],
            nuitka_version=file_info[1],
            python_version=file_info[2],
            file_json=file_json,
            nuitka_stats=parsed_stats["nuitka"],
            cpython_stats=parsed_stats["cpython"],
            benchmark_name=benchmark_name.strip("bm_"),
        )

    def __str__(self) -> str:
        return f"{self.target} - {self.nuitka_version} - {self.python_version}"

    def __repr__(self) -> str:
        return f"Benchmark(target={self.target}, nuitka_version={self.nuitka_version}, python_version={self.python_version})"


BENCHMARK_DIRECTORY = Path("benchmarks")

results_container: dict[tuple[int, int], list[Benchmark]] = {}

for benchmark_item in BENCHMARK_DIRECTORY.iterdir():
    if benchmark_item.is_dir() and not benchmark_item.name.startswith("bm_"):
        continue

    results = benchmark_item / "results"
    for date in results.iterdir():
        if not date.is_dir():
            continue

        for result in date.iterdir():
            if not result.is_file():
                continue

            benchmark_result = Benchmark.from_path(result, benchmark_item.name)

            results_container.setdefault(benchmark_result.python_version, []).append(
                benchmark_result
            )


def format_benchmark_stat(nuitka, cpython) -> str:
    if nuitka < cpython:
        percentage = (cpython / nuitka) * 100 - 100
        return f"{nuitka:.2f} +[green]{percentage:.2f}%[/green]"

    elif nuitka > cpython:
        percentage = (nuitka / cpython) * 100 - 100
        return f"{nuitka:.2f} -[red]{percentage:.2f}%[/red]"
    else:
        return f"{nuitka:.2f}"


sorted_results = sorted(results_container.items(), key=lambda x: x[0], reverse=True)

Bench_table = Table(title="Benchmarks")
Bench_table.add_column("Benchmark", justify="center")
Bench_table.add_column("Cpython Version", justify="center")
Bench_table.add_column("Nuitka Release", justify="center")
Bench_table.add_column("Nuitka Factory", justify="center")

# Bench_table.add_column("CPython", justify="center")
Bench_table.add_column("faster", justify="center")
# Bench_table.add_column("Percentage", justify="center")

sorted_results = sorted(results_container.items(), key=lambda x: x[0], reverse=True)
for python_version, benchmarks in sorted_results:

    release, factory = benchmarks[0], benchmarks[1]
    # release_avg = sum(release.nuitka_stats.benchmark) / len(
    #     release.nuitka_stats.benchmark
    # )
    # factory_avg = sum(factory.nuitka_stats.benchmark) / len(
    #     factory.nuitka_stats.benchmark
    # )
    # min_release = min(release.nuitka_stats.benchmark)
    # min_factory = min(factory.nuitka_stats.benchmark)

    # cpython_avg = sum(release.cpython_stats.benchmark) / len(
    #     release.cpython_stats.benchmark
    # )
    # nuitka_avg = sum(release.nuitka_stats.benchmark) / len(
    #     release.nuitka_stats.benchmark
    # )
    # min_nuitka = min(release.nuitka_stats.benchmark)
    # min_cpython = min(release.cpython_stats.benchmark)
    # faster = "Yes" if cpython_avg > nuitka_avg else "No"

    #    min_nuitka = min(
    #         sum(bench_results["nuitka"]["benchmark"]) / ITERATIONS,
    #         sum(bench_results["nuitka"]["warmup"]) / ITERATIONS,
    #     )

    #     min_cpython = min(
    #         sum(bench_results["cpython"]["benchmark"]) / ITERATIONS,
    #         sum(bench_results["cpython"]["warmup"]) / ITERATIONS,
    #     )

    #     if min_nuitka < min_cpython:
    #         print(
    #             f"{nuitka_version} is faster for benchmark {benchmark.name} by {((min_cpython - min_nuitka) / min_cpython) * 100:.2f}%"
    #         )
    #     else:
    #         print(
    #             f"{python_version} is faster for benchmark {benchmark.name} by {((min_nuitka - min_cpython) / min_nuitka) * 100:.2f}%"
    #         )
    #     results.add_section()
    #     for key in ["warmup", "benchmark"]:
    #         results.add_row(
    #             key,
    #             f"{sum(bench_results['nuitka'][key]) / ITERATIONS:.2f}",
    #             f"{sum(bench_results['cpython'][key]) / ITERATIONS:.2f}",
    #         )
    min_release = min(
        sum(release.nuitka_stats.benchmark) / len(release.nuitka_stats.benchmark),
        sum(release.nuitka_stats.warmup) / len(release.nuitka_stats.warmup),
    )

    min_factory = min(
        sum(factory.nuitka_stats.benchmark) / len(factory.nuitka_stats.benchmark),
        sum(factory.nuitka_stats.warmup) / len(factory.nuitka_stats.warmup),
    )

    min_cpython = min(
        sum(release.cpython_stats.benchmark) / len(release.cpython_stats.benchmark),
        sum(release.cpython_stats.warmup) / len(release.cpython_stats.warmup),
        sum(factory.cpython_stats.benchmark) / len(factory.cpython_stats.benchmark),
        sum(factory.cpython_stats.warmup) / len(factory.cpython_stats.warmup),
    )

    # Bench_table.add_row(
    #     release.benchmark_name,
    #     f"{python_version[0]}.{python_version[1]}",
    #     # f"{min_release:.2f} {format_benchmark_stat(min_release, min_cpython)}",
    #     # f"{min_factory:.2f} {format_benchmark_stat(min_factory, min_cpython)}",
    #     f"{format_benchmark_stat(min_release, min_cpython)}",
    #     f"{format_benchmark_stat(min_factory, min_cpython)}",
    #     faster,
    # )

    Bench_table.add_row(
        release.benchmark_name,
        f"{python_version[0]}.{python_version[1]}",
        # f"{release.nuitka_version}",
        # f"{factory.nuitka_version}",
        f"{format_benchmark_stat(min_release, min_cpython)}",
        f"{format_benchmark_stat(min_factory, min_cpython)}",
    )

print(Bench_table)
