# Import & Export

Colvert supports importing and exporting data in various formats. This page provides an overview of the supported formats and how to use them.

[TOC]

Colvert will automatically detect the format of the file based on the file extension.

If you send multiple files to Colvert, it will try to detect if the files are part of the same table or different tables. If the files are part of the same table, Colvert will merge them into a single table. If the files are part of different tables, Colvert will create a table for each file.

This is done by looking at the file name and trying to find a common prefix. If a common prefix is found, the prefix is used as the table name. If no common prefix is found, the file name is used as the table name.

Examples: 
* `my-dataset-1.parquet` and `my-dataset-2.parquet` will be merged into a single table named `my-dataset`.
* `my-dataset-1.parquet` and `another-dataset-2.parquet` will be loaded into two separate tables named `my-dataset-1` and `another-dataset-2`.

## DuckDB

DuckDB file can be imported using the command line interface:

```bash
colvert open my-dataset.duckdb
```

Or 

```bash
colvert open --database=my-dataset.duckdb
```

The file extension `.db` is also supported.

## CSV

CSV (Comma Separated Values) is a simple text format for tabular data. Colvert supports importing data in CSV format.

### Importing CSV Files

Single CSV files can be imported using the command line interface:

```bash
colvert open my-dataset.csv
```

## JSON

JSON (JavaScript Object Notation) is a lightweight data interchange format. Colvert supports importing JSON format.

### Importing JSON Files

Single JSON files can be imported using the command line interface:

```bash
colvert open my-dataset.json
```

DuckDB will try to detect the type of JSON automatically. The following types are supported:

#### JSON array

```json
[
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]
```

#### JSON newline-delimited

```json
{"name": "Alice", "age": 30}
{"name": "Bob", "age": 25}
```

#### JSON unstructured

```json
{
    "name": "Alice",
    "age": 30
}
{
    "name": "Bob",
    "age": 25
}
```


## Parquet

Parquet is a columnar storage format that is optimized for reading and writing large datasets. Colvert supports importing and exporting data in Parquet format.

More informations about handling Parquet files can be found in the [DuckDB documentation](https://duckdb.org/docs/data/parquet).

### Importing Parquet Files

Single Parquet files can be imported using the command line interface:

```bash
colvert open my-dataset.parquet
```

Multiple Parquet files can be imported using the SQL interface:
```bash
colvert open --table=dataset my-dataset-1.parquet  my-dataset-2.parquet
```

If no table name is provided a table name will be generated based on the files name using their common prefix.