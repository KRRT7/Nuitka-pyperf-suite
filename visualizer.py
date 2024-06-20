from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.console import Group
from rich.console import Console
from Utilities import get_visualizer_setup, centered_text
from rich.terminal_theme import SVG_EXPORT_THEME

console = Console(record=True)


def build_table() -> Table:
    table = Table()
    table.add_column("Version")
    table.add_column("Cpython")
    table.add_column("Nuitka")
    table.add_column(centered_text("Diff"))

    return table


dates: dict[str, list[Table]] = {}
for name, date, benchmarks in get_visualizer_setup():
    table = build_table()

    for benchmark in benchmarks:
        nuitka_stats = benchmark.calculate_stats("nuitka")
        cpython_stats = benchmark.calculate_stats("cpython")

        table.title = name
        table.add_row(
            centered_text(benchmark.py_version),
            centered_text(f"{cpython_stats:.2f}"),
            centered_text(f"{nuitka_stats:.2f}"),
            benchmark.format_stats(),
        )
    dates.setdefault(date, []).append(table)

if not dates:
    raise SystemExit("No data to visualize")

grid = Table.grid(expand=True)
rows = []
for date, tables in dates.items():
    rows.append(Panel(Group(*tables), title=date, expand=False))
grid.add_row(*rows[-3:])

console.print(Align.center(grid))
console.save_svg("test.svg")
