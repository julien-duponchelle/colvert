# Samples

Colvert provide a set of sample datasets that you can use to get started. 

```console
colvert sample nyc_taxi
```

This will download the `nyc_taxi` dataset to the system temporary directory.

You can after open the dataset using the `colvert open` command.

```console
colvert open /tmp/nyc_taxi/*.parquet
```

## Available samples

* `nyc_taxi`: A dataset of taxi trips in New York City. The dataset is stored in parquet format.