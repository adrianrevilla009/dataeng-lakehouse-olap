# iceberg-delta

`timetravel.py` writes three versions of a Delta Lake table with delta-rs, reads an old version, then compacts the files.

## Goal

Show table-format time travel and compaction without a JVM or Spark. The folder is named after Iceberg and Delta, but only Delta Lake is implemented here.

## Run it

```
pip install -r requirements.txt
python3 timetravel.py
```

Expected: a line like `versions: 3 files: 3 -> 1` (the version number is that of the compaction commit) and `OK`.
Not run end to end: `deltalake==0.20.2` and `pyarrow==17.0.0` were not installed when this README was written, so the exact numbers on the `versions:` line are unconfirmed; the asserts in the script require the file count to drop.

## What it proves

- Three commits (version 0 with 3 rows, then two appends of 3 rows each) give a 9-row table; `DeltaTable(path, version=0)` still returns only 3 rows.
- `dt.optimize.compact()` leaves the data at 9 rows but reduces the number of data files below the count before compaction.
- History survives compaction: `DeltaTable(path, version=1)` still returns 6 rows afterwards.

## Trade-offs

- Each append creates a small file; compaction fixes that but adds a commit and rewrites data.
- Old versions stay readable only until the files they reference are vacuumed; this script does not run vacuum.
- Iceberg is not covered, so snapshot expiry and hidden partitioning are not shown.

## When not to use it

- When you need concurrent writers from Spark or Trino against a shared catalog; run the table format on that engine instead.
- For tiny tables that are rewritten whole; plain Parquet files are simpler.
