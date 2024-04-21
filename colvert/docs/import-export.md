# Import & Export

Colvert supports importing and exporting data in various formats. This page provides an overview of the supported formats and how to use them.

[TOC]

## Parquet

Parquet is a columnar storage format that is optimized for reading and writing large datasets. Colvert supports importing and exporting data in Parquet format.

More informations about handling Parquet files can be found in the [DuckDB documentation](https://duckdb.org/docs/data/parquet).

### Importing Parquet Files

Single Parquet files can be imported using the command line interface:

```bash
colvert open my-dataset.parquet
```

Multiple Parquet files can be imported using the SQL interface:
```sql
CREATE TABLE test AS SELECT * FROM read_parquet(['file1.parquet', 'file2.parquet', 'file3.parquet']);
```

