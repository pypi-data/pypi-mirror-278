from pathlib import Path
import click
import importlib.util
import sys
from rich.console import Console
from sewerpipe.workflows import get_workflow
from sewerpipe.task import Task


def magical_module_import(path: Path):
    module_name = "sewerpipe.current_workflow"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@click.command()
@click.option("-p", "--path", type=click.Path(exists=True),
              help="Path to the workflow definition file.")
@click.option("-i", "--python-interpreter", type=click.Path(),
              help="Path to the python interpreter.",
              default="python")
@click.option("-w", "--workflow", type=str,
              help="Workflow name.", default="workflow")
def run(path: Path, python_interpreter: Path, workflow: str):
    console = Console()
    console.print(f"[blue]Provided path: {path}[/blue]")

    # This blackmagic f***ery is needed to import the module from a given path:
    module = magical_module_import(path)

    # Here's where a registering decorator comes in handy:
    workflow = get_workflow(workflow)

    # Workflows can optionally return a value:
    res = workflow()

    # Print the result:
    console.print(f"[green]Workflow {workflow} has returned {res}[/green]")


@click.command()
@click.option("-p", "--path", type=click.Path(exists=True),
              help="Path to the workflow definition file.")
@click.option("-o", "--output", type=click.Path(),
                help="Path to the output file.")
@click.option("--to", type=click.Choice(["vscode", "airflow"]),
              help="Output format.")
@click.option("--print-only", is_flag=True, help="Print the output instead of writing to a file.")
@click.option("--launch-json-version", default="0.2.0", help="Version of the launch.json file.")
def convert(path: Path, output: Path, to: str, print_only: bool, launch_json_version: str):
    console = Console()
    match to:
        case "vscode":
            from sewerpipe.vscode import generate_launch_json
            module = magical_module_import(path)
            all_tasks = dict([(name, klass) for name, klass in module.__dict__.items() if isinstance(klass, Task)])
            console.print(f"[green]Found tasks: {[f'{name} ({task.name})' for name, task in all_tasks.items()]}[/green]")
            if len(all_tasks) == 0:
                console.print("[red]No tasks found in the provided module.[/red]")
                return
            ret = generate_launch_json(all_tasks.values(),
                                       output,
                                       launch_json_version,
                                       "write" if not print_only else "return")
            if print_only:
                console.print(ret)
        case "airflow":
            # from sewerpipe.airflow import create_airflow_tasks
            raise NotImplementedError("Airflow conversion is supported only in library usage.")
        case _:
            raise ValueError(f"Invalid value for 'to': {to}")


@click.group()
def main():
    pass


main.add_command(run)
main.add_command(convert)


if __name__ == "__main__":
    main()
