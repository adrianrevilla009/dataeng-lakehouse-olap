# clickhouse-olap

`orders.sql` builds a partitioned MergeTree table and a pre-aggregated AggregatingMergeTree table; `run.sh` runs it against a ClickHouse container over HTTP.

## Goal

Show ClickHouse's MergeTree storage (partitioned, sorted) and how partial aggregate states are stored and merged for fast revenue-per-customer queries.

## Run it

```
./run.sh
```

Expected: the script starts `clickhouse/clickhouse-server:24.8`, waits for `/ping`, runs each line of `orders.sql`, prints `ana	30` and `bo	5` (tab separated), then `OK`, and removes the container on exit.
Not run end to end: Docker was not started when this README was written.

## What it proves

- `orders` uses `PARTITION BY toYYYYMM(day)` and `ORDER BY (customer, day)`, the two knobs that decide how data is pruned and sorted.
- `revenue_by_customer` stores `AggregateFunction(sum, Float64)`; the final query uses `sumMerge` to turn states into numbers.
- `run.sh` compares the output to `ana 30` / `bo 5` exactly and prints `OK` only on a match.

## Trade-offs

- `run.sh` sends one statement per line, so every statement in `orders.sql` must stay on a single line.
- The aggregate table is filled once with `INSERT ... SELECT`; a materialized view would keep it up to date but is not used here.
- Security is off (`CLICKHOUSE_SKIP_USER_SETUP`) and the HTTP port 8123 is open, fine for a local lab only.

## When not to use it

- For transactional workloads with frequent updates and point lookups.
- For a single-node analytic query over a few files, DuckDB is lighter.
