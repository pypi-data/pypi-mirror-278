from pathlib import Path
import contextlib
import os


@contextlib.contextmanager
def chdir(path: Path | str):
    """Change directory to `path` and return to the original directory when done."""
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)
