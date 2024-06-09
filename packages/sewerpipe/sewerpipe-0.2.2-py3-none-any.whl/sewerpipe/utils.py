import importlib.util
import sys
from pathlib import Path
from rich.console import Console


def magical_module_import(path: Path):
    module_name = "sewerpipe.current_workflow"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
