from typing import Literal
from pathlib import Path
from statistics import mean
from json import load, dump
from dataclasses import dataclass


@dataclass
class Stats:
    name: str
    warmup: list[float]
    benchmark: list[float]

    @classmethod
    def from_dict(cls, stats_dict: dict[str, list[float]], name: str) -> "Stats":
        return cls(
            name,
            stats_dict["warmup"],
            stats_dict["benchmark"],
        )


@dataclass
class Benchmark:
    target: str | None = None
    nuitka_version: str | None = None
    python_version: tuple[int, int] | None = None
    file_json: dict[str, dict[str, list[float]]] | None = None
    nuitka_stats: Stats | None = None
    cpython_stats: Stats | None = None
    benchmark_name: str = ""

    @staticmethod
    def parse_file_name(file_name: str) -> tuple[str, str, tuple[int, int]]:
        target, nuitka_version, python_version = file_name.split("-")
        py_ver_split = python_version.split(".")
        python_version_tuple = (int(py_ver_split[0]), int(py_ver_split[1]))
        return target, nuitka_version, python_version_tuple

    @staticmethod
    def parse_stats(stats: dict[str, dict[str, list[float]]]) -> dict[str, Stats]:
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
    def from_path(
        cls, file_path: Path, benchmark_name: str, in_progess: bool = False
    ) -> "Benchmark":
        if in_progess:
            return cls(
                benchmark_name=benchmark_name,
            )

        if not file_path.stat().st_size > 0:
            raise FileNotFoundError(f"File {file_path} does not exist or is empty")

        with open(file_path, "r") as f:
            file_json = load(f)

        file_info = cls.parse_file_name(file_path.stem)
        # parsed_stats = cls.parse_stats(file_json)
        return cls(
            target=file_info[0],
            nuitka_version=file_info[1],
            python_version=file_info[2],
            file_json=file_json,
            # nuitka_stats=parsed_stats["nuitka"],
            nuitka_stats=Stats(
                "nuitka",
                file_json["nuitka"]["warmup"],
                file_json["nuitka"]["benchmark"],
            ),
            # cpython_stats=parsed_stats["cpython"],
            cpython_stats=Stats(
                "cpython",
                file_json["cpython"]["warmup"],
                file_json["cpython"]["benchmark"],
            ),
            benchmark_name=benchmark_name.removeprefix("bm_"),
        )

    @classmethod
    def from_dict(
        cls, file_dict: dict[str, dict[str, list[float]]], benchmark_name: str
    ) -> "Benchmark":
        file_info = cls.parse_file_name(benchmark_name)
        return cls(
            target=file_info[0],
            nuitka_version=file_info[1],
            python_version=file_info[2],
            file_json=file_dict,
            nuitka_stats=Stats(
                "nuitka",
                file_dict["nuitka"]["warmup"],
                file_dict["nuitka"]["benchmark"],
            ),
            cpython_stats=Stats(
                "cpython",
                file_dict["cpython"]["warmup"],
                file_dict["cpython"]["benchmark"],
            ),
            benchmark_name=benchmark_name.removeprefix("bm_"),
        )

    def to_json_file(self, file_path: Path) -> None:

        if not self.nuitka_stats or not self.cpython_stats:
            raise ValueError("Stats not found")

        contents = {
            "nuitka": {
                "warmup": self.nuitka_stats.warmup,
                "benchmark": self.nuitka_stats.benchmark,
            },
            "cpython": {
                "warmup": self.cpython_stats.warmup,
                "benchmark": self.cpython_stats.benchmark,
            },
        }
        with open(file_path, "w") as f:
            dump(contents, f)

    def calculate_stats(self, which: Literal["nuitka", "cpython"]) -> float:
        if which.lower() not in ["nuitka", "cpython"]:
            raise ValueError("Invalid value for 'which' parameter")

        if not self.nuitka_stats or not self.cpython_stats:
            raise ValueError("Stats not found")

        stats = self.nuitka_stats if which.lower() == "nuitka" else self.cpython_stats

        is_warmup_skewed: bool = min(stats.warmup) == stats.warmup[0]
        is_benchmark_skewed: bool = min(stats.benchmark) == stats.benchmark[0]

        warmup = mean(stats.warmup[is_warmup_skewed:])
        benchmark = mean(stats.benchmark[is_benchmark_skewed:])

        return min(warmup, benchmark)