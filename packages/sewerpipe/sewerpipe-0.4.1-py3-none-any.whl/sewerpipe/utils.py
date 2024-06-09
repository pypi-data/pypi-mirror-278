import importlib
import importlib.util
import sys
from pathlib import Path
from rich.console import Console


def load_module(path: Path | str):
    if isinstance(path, str):
        module_name = path
        module = importlib.import_module(module_name)
        spec = importlib.util.find_spec(module_name)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    else:
        module_name = "sewerpipe.current_workflow"
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    return module
