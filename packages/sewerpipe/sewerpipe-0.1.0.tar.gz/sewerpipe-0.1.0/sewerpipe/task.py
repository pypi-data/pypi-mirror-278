from pathlib import Path
from pydantic import BaseModel
from typing import Dict
from rich.console import Console
from dataclasses import dataclass
import subprocess

@dataclass
class Task:
    name: str
    module: str
    parameters_and_flags: Dict[str, str | bool]
    use_underscores: bool = False

    def __post_init__(self):
        self._parameters = {}
        self._flags = []
        self._get_flags_and_params()

    def _get_flags_and_params(self):
        for k, v in self.parameters_and_flags.items():
            if isinstance(v, bool):
                if v:
                    self._flags.append(k)
            else:
                self._parameters[k] = v

    @property
    def parameters(self):
        list_of_tuples = [
            (f"--{k.replace('_', '-')}", f"{v}") if not self.use_underscores else (f"--{k}", f"{v}")
            for k, v in self._parameters.items()
        ]
        # flatten: 
        return [j
                for i in list_of_tuples
                for j in i]

    @property
    def flags(self):
        return [
            f"--{flag.replace('_', '-')}" if not self.use_underscores else f"--{flag}"
            for flag in self._flags
        ]

    def run(self, path_to_python: Path = Path("python")):
        console = Console()
        console.print(f"[green bold]Running {self.name}...[/green bold]")
        proc = subprocess.run([str(path_to_python), "-m", self.module, *self.parameters, *self.flags], check=True)
        return proc.returncode

    def __rshift__(self, other):
        return TaskChain(self, other)


@dataclass
class TaskChain:
    left: Task
    right: Task

    def run(self):
        self.left.run()
        self.right.run()

    def __rshift__(self, other):
        return TaskChain(self, other)
