# Sewerpipe

Sewerpipe lets you define workflows based entirely on running Python modules as tasks:


```python
from sewer.config import Task
from sewer.workflows import workflow

t1 = Task(
    name="Example 1",
    module="sewer.dummy",
    parameters_and_flags=dict(
        verbose=True,
        name="My momma"
    )
)

t2 = Task(
    name="Example 2",
    module="sewer.dummy",
    parameters_and_flags=dict(
        verbose=False,
        name="My momma not"
    )
)


@workflow
def workflow():
    (t1 >> t2).run()


def main():
    workflow()


if __name__ == "__main__":
    main()
```

The syntax is similar to Airflow DAGs, quite intentionally. There are three ways to use it:
- Direct triggering of workflows via `sppe run`
- Conversion of the defined workflows to VSCode `launch.json`, so that your debug configuration is up to date with what is defined as a single-source-of-truth workflow (`sppe convert --to vscode`)
- Library use to enable seamless creation of Airflow DAGs (via the `airflow.create_airflow_tasks` function or direct import under `@task` or `@task.external_python` decorators)

> [!note]
> Using `>>` is purely syntactic sugar here. Also, you're free to run arbitrary functions under the `workflow` definition, but it kind of defeats the purpose of the project.

> [!warning]
> The `Task` defnition currently only supports running properly installed Python modules (I'm using `python -m` underneath). I am of the strong opinion that proper packaging practices will alleviate most of your pains working with Python, so I am not planning support for running arbitrary scripts (i.e. `python something.py`). Also the equivalent of a `BashOperator` in Airflow is not implemented and I am not sure whether it would be a good idea in the first place. If you have any use-cases I'm open to discussion.


## Examples

### Data generation pipeline

For one of my projects I needed to generate synthetic data and I wanted to have the option to run the script directly on the target node using Remote SSH extension in VSCode and the Python Debugger, as well as being able to seamlessly run the exact same workflow either from the command line (e.g. in a Tmux session) or in Airflow.

#### Running from the command line

In a `tmux` session or directly in the Bash terminal you can run the following:

```bash
sppe run -p workflows/example.py
```

Provided `example.py` exists under the `./workflows` directory, you should be able to run any sequence of tasks.

#### Generation of the VSCode Debugger config

You can run the following:

```bash
sppe convert -p workflows/example.py --to vscode
```

> [!note]
> By default the configuration will be written to `.vscode/launch.json`. If you need a different output path, use `--output`/`-o` option and provide custom path.

#### Creating Airflow Tasks

I have for now not implemented Airflow DAG generation, just creation of individual tasks. I might consider that in the future, I also welcome pull requests, provided the changes are sufficiently tested.

For my own usage, calling `airflow.create_airflow_task` is sufficient, since the focus here is on debuggability of individual tasks, not of the entire DAG. And there might be slight differences in local env vs. Airflow's env.

First, tasks can be imported directly and this can be done under an external Python interpreter:

```python
@task.external_python(python="/home/chris/anaconda3/envs/someenv/bin/python")
def data_generation(gpu_index: int):
    import sys
    from pathlib import Path
    from somefolder.workflows.data_generation import t1
    t1.run(path_to_python=Path(sys.executable))
```

You can also of course wrap an entire Sewerpipe workflow under one Airflow task:

```python
@task.external_python(python="/home/chris/anaconda3/envs/someenv/bin/python")
def data_generation(gpu_index: int):
    import sys
    from pathlib import Path
    from somefolder.workflows.data_generation import workflow
    workflow()
```

> [!note]
> This is not recommended because you lose separation between different tasks in the Airflow graph. But if you want to run the exact same definition of a workflow, you can do it this way.

You can use some syntactic sugar that I've added here to make working with Python-based tasks more seamless:

```python
from pathlib import Path
from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from sewerpipe.utils import load_module
from sewerpipe.task import get_task_from_module
from sewerpipe.airflow import create_airflow_task


def get_tasks(gpu_index: int):
    module = load_module(Path("/home/chris/somefolder/workflows/data_generation.py"))

    t1 = get_task_from_module(module, "data_generation")
    t2 = get_task_from_module(module, "data_noising")

    python_interpreter = Path("/home/chris/anaconda3/envs/someenv/bin/python")
    workdir = Path("/home/chris/somefolder")
    env = {"CUDA_VISIBLE_DEVICES": str(gpu_index)}

    callargs = dict(
        path_to_python=python_interpreter, env=env, workdir=workdir
    )

    _t1 = create_airflow_task(t1, **callargs)
    _t2 = create_airflow_task(t2, **callargs)

    return _t1, _t2


@task
def clean_up():
    # Your clean-up implementation
    print("Cleaning up...")


with DAG(
    'data_prep',
    description='Data preparation pipeline',
    schedule_interval=None,
) as dag:

    data_generation, data_noising = get_tasks(0)
    data_generation() >> data_noising() >> clean_up()
```

Equivalently:


```python
from pathlib import Path
from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago

python_interpreter = Path("/home/chris/anaconda3/envs/someenv/bin/python")
workdir = Path("/home/chris/somefolder")


@task.external_python(python=python_interpreter)
def data_generation(gpu_index, workdir):  # cannot use type-hints here!
    import sys
    from pathlib import Path
    from uarr.workflows.data_generation import t1
    env = {"CUDA_VISIBLE_DEVICES": str(gpu_index)}
    t1.run(path_to_python=sys.executable, workdir=workdir, env=env)


@task.external_python(python=python_interpreter)
def data_noising(gpu_index, workdir):
    import sys
    from pathlib import Path
    from uarr.workflows.data_generation import t2
    env = {"CUDA_VISIBLE_DEVICES": str(gpu_index)}
    t2.run(path_to_python=sys.executable, workdir=workdir, env=env)


@task
def clean_up():
    # Your clean-up implementation
    print("Cleaning up...")


with DAG(
    'data_prep_secondary',
    description='Data preparation pipeline',
    schedule_interval=None,
) as dag:

    gpu_available = 0

    data_generated = data_generation(gpu_available, workdir)
    data_noised = data_noising(gpu_available, workdir)

    gpu_available >> data_generated >> data_noised >> clean_up()
```

Which style of specifying Airflow Workflows you prefer is up to you. I find the prior less verbose but the latter is arguably more readable.

> [!note]
> The former solution does not use `@task.external_python` but still provides a secondary path to a different interpreter. If you despise this decorator like I do (because you literally need to do imports within the decorated tasks, as it's being sent to a different instance of the interpreter), you will probably end up using the former pattern more.
