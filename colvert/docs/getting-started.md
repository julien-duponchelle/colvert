# Getting Started

Colvert is a browser based data analysis tool that allows you to import, and visualize data using SQL queries. This guide will walk you through the basics of using Colvert.

## Importing Data

To get started, you will need to import some data. You can import data from a CSV file, JSON file or a parquet file.

```console
$ colvert open data.csv
```

This will open the data in a memory table that you can query using SQL. Your browser should open to the Colvert interface where you can start writing queries.

!!! warning
    At this point the data is only stored in memory. If close you Colvert, you will lose the data.

The table name will be the same as the file name without the extension. You can also specify a table name using the `--table` option.

```console
$ colvert open --table my_table data.csv
```