# trino-duckdb

`duck.py` writes Orders to a Parquet file, aggregates it with DuckDB, and can run the same SQL on a Trino container with the memory connector.

## Goal

Show the same per-customer aggregate over Parquet files in an embedded engine (DuckDB) and in a distributed SQL engine (Trino), using identical SQL text.

## Run it

```
pip install -r requirements.txt
python3 duck.py

# optional: also run on Trino
docker compose up -d
WITH_TRINO=1 python3 duck.py
docker compose down -v
```

Expected: `duckdb: [('ana', 2, 30.0), ('bo', 1, 5.0)]` then `OK`; with `WITH_TRINO=1` an extra `trino:` line with the same two rows as lists.
Not run end to end: `duckdb==1.1.3` was not installed and Docker was not started when this README was written. Trino may need a short wait after `up -d` before it accepts statements.

## What it proves

- `duck()` writes three orders to a temporary Parquet file and queries it with `read_parquet(...)`; an assert compares the result to `EXPECTED`.
- The Trino path posts the statement to `/v1/statement` and follows `nextUri` until rows arrive, using only the standard library.
- Trino here reads the memory connector (`memory.properties`), not the Parquet file, so the engines share SQL but not storage.

## Trade-offs

- The memory connector loses its data when the container stops, which keeps the lab small but is not how Trino is used on a lake.
- The Trino check prints its rows but does not assert them.
- DuckDB is single-node; Trino adds coordination overhead that only pays off on large data.

## When not to use it

- For data that fits on one machine, DuckDB alone is enough.
- As a Trino benchmark: the dataset has three rows.
