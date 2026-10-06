"""Delta Lake time travel and compaction with the delta-rs Python binding (no JVM, no Spark)."""
import tempfile

import pyarrow as pa
from deltalake import DeltaTable, write_deltalake


def batch(start, n):
    return pa.table({"order_id": list(range(start, start + n)), "total": [float(i) for i in range(n)]})


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as path:
        write_deltalake(path, batch(1, 3))                  # version 0
        write_deltalake(path, batch(4, 3), mode="append")   # version 1
        write_deltalake(path, batch(7, 3), mode="append")   # version 2

        assert DeltaTable(path, version=0).to_pyarrow_table().num_rows == 3   # time travel
        assert DeltaTable(path).to_pyarrow_table().num_rows == 9

        dt = DeltaTable(path)
        files_before = len(dt.files())
        dt.optimize.compact()                               # many small files -> one
        dt = DeltaTable(path)
        assert len(dt.files()) < files_before, (files_before, len(dt.files()))
        assert dt.to_pyarrow_table().num_rows == 9          # data unchanged
        assert DeltaTable(path, version=1).to_pyarrow_table().num_rows == 6  # history survives compaction
        print("versions:", dt.version(), "files:", files_before, "->", len(dt.files()))
        print("OK")
