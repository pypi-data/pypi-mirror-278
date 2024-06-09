from sewerpipe.config import Config
from rich.console import Console


def list_tasks(config: Config):
    console = Console()
    for job in config.tasks:
        console.print(job.name)
