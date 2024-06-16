from rich import print
from rich.table import Table
from rich.panel import Panel

# from rich.
from rich.console import Group
from rich.console import Console
from Utilities import get_visualizer_setup
from rich.terminal_theme import SVG_EXPORT_THEME

console = Console(record=True)


def build_table() -> Table:
    table = Table()
    table.add_column("Version")
    table.add_column("Cpython")
    table.add_column("Nuitka")
    table.add_column("Difference")

    return table


dates: dict[str, list[Table]] = {}
for name, date, benchmarks in get_visualizer_setup():
    table = build_table()

    for benchmark in benchmarks:
        nuitka_stats = benchmark.calculate_stats("nuitka")
        cpython_stats = benchmark.calculate_stats("cpython")

        table.title = name
        table.add_row(
            "{}.{}".format(benchmark.python_version[0], benchmark.python_version[1]),  # type: ignore
            f"{cpython_stats:.2f}",
            f"{nuitka_stats:.2f}",
            benchmark.format_stats(),
        )
    dates.setdefault(date, []).append(table)

for date, tables in dates.items():
    console.print(Panel(Group(*tables), title=date, expand=False))

console.save_html("test.html", theme=SVG_EXPORT_THEME)
