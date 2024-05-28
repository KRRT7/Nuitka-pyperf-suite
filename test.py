from Utilities import (
    temporary_directory_change,
    resolve_venv_path,
    run_benchmark,
    parse_py_launcher,
    create_venv_with_version,
)


# ITERATIONS = 100


versions = parse_py_launcher()
nuitka_versions = ['"https://github.com/Nuitka/Nuitka/archive/develop.zip"', 'nuitka']



# yield each version of python, and and one of each nuitka version

for python_version in versions:
    for nuitka_version in nuitka_versions:
        print(f"Python version: {python_version}, Nuitka version: {nuitka_version}")
