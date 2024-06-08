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
