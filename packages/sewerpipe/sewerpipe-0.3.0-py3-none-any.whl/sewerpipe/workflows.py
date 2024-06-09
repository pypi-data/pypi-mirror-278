from rich.console import Console


REGISTERED_WORKFLOWS = {}


def workflow(func):
    console = Console()
    def wrapper(*args, **kwargs):
        console.print(f"[blue]Running workflow {func.__name__}[/blue]")
        func(*args, **kwargs)
    REGISTERED_WORKFLOWS[func.__name__] = wrapper
    return wrapper


def get_workflow(name):
    return REGISTERED_WORKFLOWS[name]
