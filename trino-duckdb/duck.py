"""Query Parquet files in place with DuckDB, then run the same aggregate on Trino if it is up."""
import json
import os
import tempfile
import urllib.request

import duckdb

SQL = "SELECT customer, count(*) AS orders, sum(total) AS revenue FROM {src} GROUP BY customer ORDER BY customer"
EXPECTED = [("ana", 2, 30.0), ("bo", 1, 5.0)]


def duck(path):
    con = duckdb.connect()
    con.execute(f"COPY (SELECT * FROM (VALUES (1,'ana',10.0::DOUBLE),(2,'ana',20.0),(3,'bo',5.0)) t(order_id, customer, total)) "
                f"TO '{path}' (FORMAT parquet)")
    return con.execute(SQL.format(src=f"read_parquet('{path}')")).fetchall()


def trino(sql):
    """Trino REST protocol: POST the statement, then follow nextUri until the rows arrive."""
    req = urllib.request.Request("http://localhost:8080/v1/statement", sql.encode(), {"X-Trino-User": "lab"})
    body, rows = json.load(urllib.request.urlopen(req)), []
    while "nextUri" in body:
        rows += body.get("data", [])
        body = json.load(urllib.request.urlopen(urllib.request.Request(body["nextUri"], headers={"X-Trino-User": "lab"})))
    return rows + body.get("data", [])


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        got = duck(os.path.join(tmp, "orders.parquet"))
    assert got == EXPECTED, got
    print("duckdb:", got)
    if os.environ.get("WITH_TRINO"):
        # memory connector: load the same rows, then aggregate with the same SQL text
        trino("CREATE TABLE memory.default.orders AS SELECT * FROM (VALUES (1,'ana',10.0),(2,'ana',20.0),(3,'bo',5.0)) t(order_id, customer, total)")
        print("trino:", trino(SQL.format(src="memory.default.orders")))
    print("OK")
