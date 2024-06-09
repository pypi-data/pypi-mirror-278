import sys
from typing import Dict
from pathlib import Path
from datetime import datetime
from airflow.decorators import task
from sewerpipe.task import Task


def create_airflow_task(task_sp: Task,
                        path_to_python: Path = Path("python"),
                        env: Dict[str, str] | None = None,
                        workdir: Path = Path.cwd()):
    @task(task_id=task_sp.name)
    def _task():
        task_sp.run(path_to_python=sys.executable if path_to_python == Path("python") else path_to_python,
                    env=env,
                    workdir=workdir)
    return _task


def create_airflow_tasks(tasks: list[Task]):
    return (create_airflow_task(task) for task in tasks)
