# dataeng-lakehouse-olap

Five small labs on the lakehouse and OLAP side of data engineering (Parquet and Avro schema evolution, Delta time travel, DuckDB and Trino, ClickHouse, Glue on LocalStack), all using the same tiny Orders data.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`parquet-avro`](./parquet-avro) | Adding a column in Parquet (pyarrow) and Avro (fastavro) without rewriting old files | `python3 evolve.py` |
| [`iceberg-delta`](./iceberg-delta) | Delta Lake time travel and compaction with delta-rs, no JVM or Spark | `python3 timetravel.py` |
| [`trino-duckdb`](./trino-duckdb) | One aggregate over Parquet in DuckDB, optionally repeated on Trino | `python3 duck.py` |
| [`clickhouse-olap`](./clickhouse-olap) | ClickHouse MergeTree and AggregatingMergeTree, driven over HTTP | `./run.sh` |
| [`aws-glue-athena-lake`](./aws-glue-athena-lake) | A Parquet table registered in the Glue Data Catalog on LocalStack | `docker compose up -d` then `python3 lake.py` |

## Prerequisites

- Python 3.10 or newer with `pip`; each Python folder pins its packages in `requirements.txt`.
- Docker with the Compose plugin (`clickhouse-olap`, `aws-glue-athena-lake`, and optionally `trino-duckdb`).
- `curl` and `bash` for `clickhouse-olap/run.sh`.

## How to read it

Start with `parquet-avro`, then `iceberg-delta` for table-level versioning. The remaining folders are independent. None of the scripts were run end to end while writing these READMEs; each folder README says what to expect.
