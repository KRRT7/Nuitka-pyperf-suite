from rich import print
from rich.table import Table
from rich.panel import Panel
# from rich.
from rich.console import Group
from rich.console import Console
from Utilities import get_visualizer_setup
from rich.terminal_theme import SVG_EXPORT_THEME
console = Console(record=True)
group = []
# for name, date, benchmarks in get_visualizer_setup(test=True):
for name, date, benchmarks in get_visualizer_setup():

    table = Table(title=f"[bold]{name}[/bold]", show_header=True)

    table.add_column("Version")
    table.add_column("Cpython")
    table.add_column("Nuitka")
    table.add_column("Difference")

    for benchmark in benchmarks:
        nuitka_stats = benchmark.calculate_stats("nuitka")
        cpython_stats = benchmark.calculate_stats("cpython")

        table.add_row(
            "{}.{}".format(benchmark.python_version[0], benchmark.python_version[1]),  # type: ignore
            f"{benchmark.calculate_stats('cpython'):.2f}",
            f"{benchmark.calculate_stats('nuitka'):.2f}",
            benchmark.format_stats(),
        )

    # print(Panel(table, expand=False))
    group.append(table)
# print(Group(*group))
console.print(Group(*group))

console.save_html("test.html", theme=SVG_EXPORT_THEME)