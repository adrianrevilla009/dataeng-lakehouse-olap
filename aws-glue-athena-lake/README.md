# aws-glue-athena-lake

`lake.py` creates an S3 bucket and registers a partitioned Parquet `orders` table in the Glue Data Catalog on LocalStack.

## Goal

Show how a data lake table is described in Glue (columns, partition key, location, Parquet serde), which is the metadata Athena reads, without touching a real AWS account.

## Run it

```
pip install -r requirements.txt
docker compose up -d
python3 lake.py
docker compose down -v
```

Expected: `catalog table: orders s3://orders-lake/orders/` then `OK`. LocalStack may need a few seconds after `up -d` before the script connects.
Not run end to end: `boto3==1.35.36` was not installed and Docker was not started when this README was written. Athena queries are not part of this folder; only the catalog entry is created.

## What it proves

- `compose.yaml` runs `localstack/localstack:3.8` with only `s3` and `glue`; `lake.py` talks to `http://localhost:4566` with dummy credentials.
- The `shop.orders` table has columns `order_id`, `customer`, `total`, partition key `day`, and the Hive Parquet input, output and serde classes.
- An assert reads the table back with `get_table` and checks the column names.

## Trade-offs

- No Parquet files are uploaded, so the table is registered but empty and no partitions exist.
- Re-running the script fails because the bucket and database already exist; recreate the container first.
- Cost: none locally. On real AWS the Glue catalog and S3 storage are billed, and Athena bills per data scanned.

## When not to use it

- To learn Athena query behaviour or pricing; that needs the real service.
- If you already manage tables with Iceberg or Delta, whose metadata lives with the data.
