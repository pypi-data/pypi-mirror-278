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
- Library use to enable seamless creation of Airflow DAGs (via the `airflow.create_airflow_tasks` function)

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

I have for now not implemented Airflow DAG generation, just creation of individual tasks. I might consider that in the future.

For my own usage, calling `airflow.create_airflow_tasks` is sufficient, since the focus here is on debuggability of individual tasks, not of the entire DAG. And there might be slight differences in local env vs. Airflow's env. So for now this is going to work somewhat like this:

- [ ] todooooo
