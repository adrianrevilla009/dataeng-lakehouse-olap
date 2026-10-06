# parquet-avro

`evolve.py` adds a `currency` column to the Orders schema and reads old data with the new schema in both Parquet and Avro.

## Goal

Show backward-compatible schema evolution (adding a column) in Parquet and Avro, and how each format fills the value for rows written before the column existed.

## Run it

```
pip install -r requirements.txt
python3 evolve.py
```

Expected: a `parquet:` line with three rows where order 1 and 2 have `currency` None and order 3 has `USD`, an `avro:` line with one row whose `currency` is `EUR`, then `OK`.
Not run end to end: the packages (`pyarrow==17.0.0`, `fastavro==1.9.7`) were not installed when this README was written. The expected output follows from the assertions in the script.

## What it proves

- Parquet: `v1.parquet` (three columns) and `v2.parquet` (four columns) sit in one directory; opening it as a dataset with the V2 schema returns NULL for `currency` on the old rows.
- Avro: the file is written with `AVRO_V1`, which is embedded in the file; reading it with `AVRO_V2` fills `currency` from the field default `"EUR"`.
- Both checks are `assert` statements in `evolve.py`, so a broken evolution fails the script instead of printing `OK`.

## Trade-offs

- Parquet evolution is by column name and handled by the reader; renames and type changes need explicit handling.
- Avro needs a default on every added field, and needs the schema to travel with the data (embedded in the file here, a registry in streaming).
- The data lives in a temporary directory, so nothing is left to inspect after the run.

## When not to use it

- When a table format such as Delta or Iceberg already tracks the schema (see `iceberg-delta`), use its own schema evolution instead.
- For row-oriented streaming, where a schema registry compatibility check is the real contract.
