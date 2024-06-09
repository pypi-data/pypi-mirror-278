from typing import List, Dict, Literal
from pathlib import Path
import json
from rich.console import Console
from sewerpipe.task import Task


def generate_launch_json(tasks: List[Task] | Task,
                         launch_json_path: Path = ".vscode/launch.json",
                         launch_json_version: str = "0.2.0",
                         return_or_write: Literal["return", "write"] = "write",
                         debugger_type: Literal["python", "debugpy"] = "debugpy"):
    console = Console()
    if isinstance(tasks, Task):
        tasks = [tasks]
    launch_config = {
        "version": launch_json_version,
        "configurations": [
            {
                "name": f"{wfcfg.name}",
                "type": debugger_type,
                "request": "launch",
                "module": f"{wfcfg.module}",
                "args": wfcfg.parameters + wfcfg.flags,
                "console": "integratedTerminal"
            }
        for wfcfg in tasks]
    }

    match return_or_write:
        case "write":
            console.print(f"[blue]Writing launch.json to {launch_json_path}[/blue]")
            with open(launch_json_path, 'w') as file:
                json.dump(launch_config, file, indent=4)
        case "return":
            return launch_config
        case _:
            raise ValueError(f"Invalid value for return_or_write: {return_or_write}")


if __name__ == "__main__":
    generate_launch_json('workflow_config.json', '.vscode/launch.json')
