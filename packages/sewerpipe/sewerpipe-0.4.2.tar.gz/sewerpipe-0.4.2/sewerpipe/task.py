import sys
from pathlib import Path
from pydantic import BaseModel
from typing import Dict
from rich.console import Console
from dataclasses import dataclass
from subprocess import Popen, PIPE
from sewerpipe.changedir import chdir

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

    def run(self, path_to_python: Path = Path("python"), env: Dict[str, str] | None = None, workdir: Path = None):
        console = Console()
        console.print(f"[green bold]Running {self.name}...[/green bold]")
        if workdir is None:
            workdir = Path.cwd()
        with chdir(workdir):
            console.print(f"[green]Working directory: {workdir}[/green]")
            command = [str(path_to_python), "-m", self.module, *self.parameters, *self.flags]
            stderr_contents = ""
            with Popen(command, stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True, env=env) as proc:
                for line in proc.stdout:
                    console.print(line, end="")
                for line in proc.stderr:
                    stderr_contents += line + "\n"
        if proc.returncode != 0:
            console.print(f"[red]Task {self.name} failed with return code {proc.returncode}[/red]")
            console.print(f"[red]Command: {proc.args}[/red]")
            console.print(f"[red]Error: {stderr_contents}[/red]")
            raise ValueError(f"Task {self.name} failed with return code {proc.returncode}")
        return proc.returncode

    def __rshift__(self, other):
        return TaskChain(self, other)


@dataclass
class TaskChain:
    left: Task
    right: Task

    def run(self, path_to_python: Path = Path("python")):
        self.left.run(path_to_python)
        self.right.run(path_to_python)

    def __rshift__(self, other):
        return TaskChain(self, other)


def get_tasks_from_module(module):
    """Retrieves all task definitions from a loaded Python module."""
    console = Console()
    all_tasks = dict([(name, klass) for name, klass in module.__dict__.items() if isinstance(klass, Task)])
    console.print(f"[green]Found tasks: {[f'{name} ({task.name})' for name, task in all_tasks.items()]}[/green]")
    if len(all_tasks) == 0:
        console.print("[red]No tasks found in the provided module.[/red]")
        return dict()
    return all_tasks


def get_task_from_module(module, task_name: str):
    """Retrieves a task definition from a loaded Python module."""
    tasks_found = get_tasks_from_module(module).values()
    tasks_dict = {task.name: task for task in tasks_found}
    task = tasks_dict.get(task_name, None)
    if task is None:
        raise ValueError(f"Task {task_name} not found in the provided module.")
    return task
