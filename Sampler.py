from typing import Any, Literal
from pathlib import Path
from statistics import mean
from json import load
from dataclasses import dataclass


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

    def calculate_stats(self, which: Literal["nuitka", "cpython"]) -> float:
        stats = self.nuitka_stats if which == "nuitka" else self.cpython_stats

        is_warmup_skewed: bool = min(stats.warmup) == stats.warmup[0]
        is_benchmark_skewed: bool = min(stats.benchmark) == stats.benchmark[0]

        warmup = mean(stats.warmup[is_warmup_skewed:])
        benchmark = mean(stats.benchmark[is_benchmark_skewed:])

        return min(warmup, benchmark)
