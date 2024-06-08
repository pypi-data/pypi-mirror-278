from pathlib import Path
from datetime import datetime
from airflow.decorators import task as airflow_task
from sewerpipe.task import Task


def create_airflow_task(task: Task,
                        path_to_python: Path = Path("python")):
    if str(path_to_python) == "python":
        @airflow_task(task_id=task.name)
        def _task():
            task.run()
    else:
        @airflow_task.external_python(task_id=task.name, python_path=path_to_python)
        def _task():
            task.run(path_to_python=path_to_python)
    return _task


def create_airflow_tasks(tasks: list[Task],
                         path_to_python: Path = Path("python")):
    return (create_airflow_task(task, path_to_python) for task in tasks)
