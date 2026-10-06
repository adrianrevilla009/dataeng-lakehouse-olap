"""Schema evolution in Parquet (pyarrow) and Avro (fastavro) over the shared Orders domain."""
import io
import os
import tempfile

import fastavro
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq

V1 = pa.schema([("order_id", pa.int64()), ("customer", pa.string()), ("total", pa.float64())])
V2 = V1.append(pa.field("currency", pa.string()))  # added column

AVRO_V1 = {"type": "record", "name": "Order", "fields": [
    {"name": "order_id", "type": "long"}, {"name": "customer", "type": "string"},
    {"name": "total", "type": "double"}]}
AVRO_V2 = {"type": "record", "name": "Order", "fields": AVRO_V1["fields"] + [
    {"name": "currency", "type": "string", "default": "EUR"}]}


def parquet_demo(tmp):
    pq.write_table(pa.table({"order_id": [1, 2], "customer": ["ana", "bo"], "total": [10.0, 20.5]}, V1),
                   os.path.join(tmp, "v1.parquet"))
    pq.write_table(pa.table({"order_id": [3], "customer": ["cy"], "total": [7.0], "currency": ["USD"]}, V2),
                   os.path.join(tmp, "v2.parquet"))
    rows = ds.dataset(tmp, format="parquet", schema=V2).to_table().sort_by("order_id").to_pylist()
    assert rows[0]["currency"] is None and rows[2]["currency"] == "USD", rows  # old files read as NULL
    return rows


def avro_demo():
    buf = io.BytesIO()
    fastavro.writer(buf, AVRO_V1, [{"order_id": 1, "customer": "ana", "total": 10.0}])
    buf.seek(0)
    rows = list(fastavro.reader(buf, reader_schema=AVRO_V2))  # writer schema is embedded in the file
    assert rows[0]["currency"] == "EUR", rows  # reader default fills the new field
    return rows


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        print("parquet:", parquet_demo(tmp))
    print("avro:", avro_demo())
    print("OK")
