# Import & Export

Colvert supports importing and exporting data in various formats. This page provides an overview of the supported formats and how to use them.

[TOC]

Colvert will automatically detect the format of the file based on the file extension.

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