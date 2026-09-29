"""Copy the root ventilation.py into every Lambda CodeUri, then sam build.

Lambda can only import from inside its own CodeUri. The copies are gitignored;
tests/test_api.py fails if any copy drifts from the root file.
"""
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE_DIRS = [HERE / "src"]  # every CodeUri in template.yaml

for d in CODE_DIRS:
    shutil.copyfile(HERE.parent / "ventilation.py", d / "ventilation.py")
subprocess.run(["sam", "build"], cwd=HERE, check=True)
