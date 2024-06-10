# Data Utility: _Workflow_

[![test](https://github.com/ddeutils/ddeutil-workflow/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/ddeutils/ddeutil-workflow/actions/workflows/tests.yml)
[![python support version](https://img.shields.io/pypi/pyversions/ddeutil-workflow)](https://pypi.org/project/ddeutil-workflow/)
[![size](https://img.shields.io/github/languages/code-size/ddeutils/ddeutil-workflow)](https://github.com/ddeutils/ddeutil-workflow)

**Table of Contents**:

- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Connection](#connection)
  - [Dataset](#dataset)
  - [Schedule](#schedule)
- [Examples](#examples)
  - [Python](#python)
  - [Tasks (EL)](#tasks-extract--load)
  - [Hooks (T)](#hooks-transform)

This **Utility Workflow** objects was created for easy to make a simple metadata
driven pipeline that able to **ETL, T, EL, or ELT** by `.yaml` file.

I think we should not create the multiple pipeline per use-case if we able to
write some dynamic pipeline that just change the input parameters per use-case
instead. This way we can handle a lot of pipelines in our orgs with metadata only.
It called **Metadata Driven**.

Next, we should get some monitoring tools for manage logging that return from
pipeline running. Because it not show us what is a use-case that running data
pipeline.

> [!NOTE]
> _Disclaimer_: I inspire the dynamic statement from the GitHub Action `.yml` files
> and all of config file from several data orchestration framework tools from my
> experience on Data Engineer.

## Installation

```shell
pip install ddeutil-workflow
```

This project need `ddeutil-io`, `ddeutil-model` extension namespace packages.

## Getting Started

The first step, you should start create the connections and datasets for In and
Out of you data that want to use in pipeline of workflow. Some of this component
is similar component of the **Airflow** because I like it concepts.

The main feature of this project is the `Pipeline` object that can call any
registries function. The pipeline can handle everything that you want to do, it
will passing parameters and catching the output for re-use it to next step.

> [!IMPORTANT]
> In the future of this project, I will drop the connection and dataset to
> dynamic registries instead of main features because it have a lot of maintain
> vendor codes and deps. (I do not have time to handle this features)

### Connection

The connection for worker able to do any thing.

```yaml
conn_postgres_data:
  type: conn.Postgres
  url: 'postgres//username:${ENV_PASS}@hostname:port/database?echo=True&time_out=10'
```

```python
from ddeutil.workflow.conn import Conn

conn = Conn.from_loader(name='conn_postgres_data', externals={})
assert conn.ping()
```

### Dataset

The dataset is define any objects on the connection. This feature was implemented
on `/vendors` because it has a lot of tools that can interact with any data systems
in the data tool stacks.

```yaml
ds_postgres_customer_tbl:
  type: dataset.PostgresTbl
  conn: 'conn_postgres_data'
  features:
    id: serial primary key
    name: varchar( 100 ) not null
```

```python
from ddeutil.workflow.vendors.pg import PostgresTbl

dataset = PostgresTbl.from_loader(name='ds_postgres_customer_tbl', externals={})
assert dataset.exists()
```

### Schedule

```yaml
schd_for_node:
  type: schedule.Schedule
  cron: "*/5 * * * *"
```

```python
from ddeutil.workflow.schedule import Schedule

scdl = Schedule.from_loader(name='schd_for_node', externals={})
assert '*/5 * * * *' == str(scdl.cronjob)

cron_iterate = scdl.generate('2022-01-01 00:00:00')
assert '2022-01-01 00:05:00' f"{cron_iterate.next:%Y-%m-%d %H:%M:%S}"
assert '2022-01-01 00:10:00' f"{cron_iterate.next:%Y-%m-%d %H:%M:%S}"
assert '2022-01-01 00:15:00' f"{cron_iterate.next:%Y-%m-%d %H:%M:%S}"
assert '2022-01-01 00:20:00' f"{cron_iterate.next:%Y-%m-%d %H:%M:%S}"
assert '2022-01-01 00:25:00' f"{cron_iterate.next:%Y-%m-%d %H:%M:%S}"
```

## Examples

This is examples that use workflow file for running common Data Engineering
use-case.

### Python

The state of doing lists that worker should to do. It be collection of the stage.

```yaml
run_py_local:
  type: ddeutil.workflow.pipe.Pipeline
  params:
    author-run:
      type: str
    run-date:
      type: datetime
  jobs:
    first-job:
      stages:
        - name: Printing Information
          id: define-func
          run: |
            x = '${{ params.author-run }}'
            print(f'Hello {x}')

            def echo(name: str):
              print(f'Hello {name}')

        - name: Run Sequence and use var from Above
          vars:
            x: ${{ params.author-run }}
          run: |
            print(f'Receive x from above with {x}')
            # Change x value
            x: int = 1

        - name: Call Function
          vars:
            echo: ${{ stages.define-func.outputs.echo }}
          run: |
            echo('Caller')
```

```python
from ddeutil.workflow.pipeline import Pipeline

pipe = Pipeline.from_loader(name='run_py_local', externals={})
pipe.execute(params={'author-run': 'Local Workflow', 'run-date': '2024-01-01'})
```

```shell
> Hello Local Workflow
> Receive x from above with Local Workflow
> Hello Caller
```

### Tasks (Extract & Load)

```yaml
pipe_el_pg_to_lake:
  type: ddeutil.workflow.pipe.Pipeline
  params:
    run-date:
      type: datetime
    author-email:
      type: str
  jobs:
    extract-load:
      stages:
        - name: "Extract Load from Postgres to Lake"
          id: extract-load
          task: tasks/postgres-to-delta@polars
          with:
            source:
              conn: conn_postgres_url
              query: |
                select * from ${{ params.name }}
                where update_date = '${{ params.datetime }}'
            sink:
              conn: conn_az_lake
              endpoint: "/${{ params.name }}"
```

### Tasks (Transform)

```yaml
pipe_hook_mssql_proc:
  type: ddeutil.workflow.pipe.Pipeline
  params:
    run_date: datetime
    sp_name: str
    source_name: str
    target_name: str
  jobs:
    transform:
      stages:
        - name: "Transform Data in MS SQL Server"
          id: transform
          task: tasks/mssql-proc@odbc
          with:
            exec: ${{ params.sp_name }}
            params:
              run_mode: "T"
              run_date: ${{ params.run_date }}
              source: ${{ params.source_name }}
              target: ${{ params.target_name }}
```

## License

This project was licensed under the terms of the [MIT license](LICENSE).
