"""Register an Orders Parquet lake in the Glue Data Catalog on LocalStack (dummy credentials, local endpoint only)."""
import boto3

ENDPOINT = "http://localhost:4566"
KW = dict(endpoint_url=ENDPOINT, region_name="eu-west-1", aws_access_key_id="test", aws_secret_access_key="test")

if __name__ == "__main__":
    s3, glue = boto3.client("s3", **KW), boto3.client("glue", **KW)
    s3.create_bucket(Bucket="orders-lake", CreateBucketConfiguration={"LocationConstraint": "eu-west-1"})
    glue.create_database(DatabaseInput={"Name": "shop"})
    glue.create_table(DatabaseName="shop", TableInput={
        "Name": "orders",
        "TableType": "EXTERNAL_TABLE",
        "PartitionKeys": [{"Name": "day", "Type": "string"}],
        "StorageDescriptor": {
            "Columns": [{"Name": "order_id", "Type": "bigint"}, {"Name": "customer", "Type": "string"},
                        {"Name": "total", "Type": "double"}],
            "Location": "s3://orders-lake/orders/",
            "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
            "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
            "SerdeInfo": {"SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"},
        }})
    got = glue.get_table(DatabaseName="shop", Name="orders")["Table"]
    assert [c["Name"] for c in got["StorageDescriptor"]["Columns"]] == ["order_id", "customer", "total"]
    print("catalog table:", got["Name"], got["StorageDescriptor"]["Location"])
    print("OK")
