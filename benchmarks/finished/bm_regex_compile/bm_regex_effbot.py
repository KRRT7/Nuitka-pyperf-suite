"""Benchmarks for Python's regex engine.

These are some of the original benchmarks used to tune Python's regex engine
in 2000 written by Fredrik Lundh. Retreived from
http://mail.python.org/pipermail/python-dev/2000-August/007797.html and
integrated into Unladen Swallow's pyperf.py in 2009 by David Laing.

These benchmarks are of interest since they helped to guide the original
optimization of the sre engine, and we shouldn't necessarily ignore them just
because they're "old".
"""

# Python imports
import re

# Local imports
# import pyperf
from time import perf_counter

USE_BYTES = False


def re_compile(s):
    if USE_BYTES:
        return re.compile(s.encode("latin1"))
    else:
        return re.compile(s)


# These are the regular expressions to be tested. These sync up,
# index-for-index with the list of strings generated by gen_string_table()
# below.


def gen_regex_table():
    return [
        re_compile("Python|Perl"),
        re_compile("Python|Perl"),
        re_compile("(Python|Perl)"),
        re_compile("(?:Python|Perl)"),
        re_compile("Python"),
        re_compile("Python"),
        re_compile(".*Python"),
        re_compile(".*Python.*"),
        re_compile(".*(Python)"),
        re_compile(".*(?:Python)"),
        re_compile("Python|Perl|Tcl"),
        re_compile("Python|Perl|Tcl"),
        re_compile("(Python|Perl|Tcl)"),
        re_compile("(?:Python|Perl|Tcl)"),
        re_compile("(Python)\\1"),
        re_compile("(Python)\\1"),
        re_compile("([0a-z][a-z0-9]*,)+"),
        re_compile("(?:[0a-z][a-z0-9]*,)+"),
        re_compile("([a-z][a-z0-9]*,)+"),
        re_compile("(?:[a-z][a-z0-9]*,)+"),
        re_compile(".*P.*y.*t.*h.*o.*n.*"),
    ]


def gen_string_table(n):
    """Generates the list of strings that will be used in the benchmarks.

    All strings have repeated prefixes and suffices, and n specifies the
    number of repetitions.
    """
    strings = []

    def append(s):
        if USE_BYTES:
            strings.append(s.encode("latin1"))
        else:
            strings.append(s)

    append("-" * n + "Perl" + "-" * n)
    append("P" * n + "Perl" + "P" * n)
    append("-" * n + "Perl" + "-" * n)
    append("-" * n + "Perl" + "-" * n)
    append("-" * n + "Python" + "-" * n)
    append("P" * n + "Python" + "P" * n)
    append("-" * n + "Python" + "-" * n)
    append("-" * n + "Python" + "-" * n)
    append("-" * n + "Python" + "-" * n)
    append("-" * n + "Python" + "-" * n)
    append("-" * n + "Perl" + "-" * n)
    append("P" * n + "Perl" + "P" * n)
    append("-" * n + "Perl" + "-" * n)
    append("-" * n + "Perl" + "-" * n)
    append("-" * n + "PythonPython" + "-" * n)
    append("P" * n + "PythonPython" + "P" * n)
    append("-" * n + "a5,b7,c9," + "-" * n)
    append("-" * n + "a5,b7,c9," + "-" * n)
    append("-" * n + "a5,b7,c9," + "-" * n)
    append("-" * n + "a5,b7,c9," + "-" * n)
    append("-" * n + "Python" + "-" * n)
    return strings


def init_benchmarks(n_values=None):
    """Initialize the strings we'll run the regexes against.

    The strings used in the benchmark are prefixed and suffixed by
    strings that are repeated n times.

    The sequence n_values contains the values for n.
    If n_values is None the values of n from the original benchmark
    are used.

    The generated list of strings is cached in the string_tables
    variable, which is indexed by n.

    Returns:
    A list of string prefix/suffix lengths.
    """

    if n_values is None:
        n_values = (0, 5, 50, 250, 1000, 5000, 10000)

    string_tables = {n: gen_string_table(n) for n in n_values}
    regexs = gen_regex_table()

    data = []
    for n in n_values:
        for id in range(len(regexs)):
            regex = regexs[id]
            string = string_tables[n][id]
            data.append((regex, string))
    return data


def bench_regex_effbot(loops):
    if bench_regex_effbot.data is None:
        bench_regex_effbot.data = init_benchmarks()
    data = bench_regex_effbot.data

    range_it = range(loops)
    search = re.search
    # t0 = pyperf.perf_counter()
    t0 = perf_counter()

    for _ in range_it:
        # Runs all of the benchmarks for a given value of n.
        for regex, string in data:
            # search 10 times
            search(regex, string)
            search(regex, string)
            search(regex, string)
            search(regex, string)
            search(regex, string)
            search(regex, string)
            search(regex, string)
            search(regex, string)
            search(regex, string)
            search(regex, string)

    # return pyperf.perf_counter() - t0
    return perf_counter() - t0


# cached data, generated at the first call
bench_regex_effbot.data = None


def add_cmdline_args(cmd, args):
    if args.force_bytes:
        cmd.append("--force_bytes")


if __name__ == "__main__":
    # runner = pyperf.Runner(add_cmdline_args=add_cmdline_args)
    # runner.metadata["description"] = (
    #     "Test the performance of regexps " "using Fredik Lundh's benchmarks."
    # )
    # runner.argparser.add_argument(
    #     "-B", "--force_bytes", action="store_true", help="test bytes regexps"
    # )
    # options = runner.parse_args()
    # if options.force_bytes:
    #     USE_BYTES = True

    # runner.bench_time_func("regex_effbot", bench_regex_effbot, inner_loops=10)
    bench_regex_effbot(10)