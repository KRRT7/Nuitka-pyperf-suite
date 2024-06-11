from pathlib import Path
import shutil

curr_dir = Path(__file__).parent

for folder in curr_dir.iterdir():
    if folder.name.startswith("bm_"):
        # go inside the folder
        for file in folder.iterdir():
            if file.is_dir() and any(
                file.name.startswith(x) for x in ["results", "run_"]
            ):
                shutil.rmtree(file)
