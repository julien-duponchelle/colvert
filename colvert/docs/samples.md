# Samples

Colvert provide a set of sample datasets that you can use to test the capabilities of the tool. 

```console
colvert sample nyc_taxi
```

This will download the `nyc_taxi` dataset to the system temporary directory.

You can after open the dataset using the `colvert open` command.

```console
colvert open /tmp/nyc_taxi/*.parquet
```

## Available samples

### New York City Taxi: nyc_taxi

A dataset of taxi trips in New York City. The dataset is stored in parquet format. It's use to demonstrate the capabilities of Colvert to handle time series data and a table split into multipe parquet files.

#### Sample request:

##### Number of trips per day

```sql
SELECT SUM(passenger_count),date_trunc('day',tpep_pickup_datetime) as date
FROM yellow_tripdata_2024
WHERE date >= '2024-01-01 00:00:00'
GROUP BY date
ORDER BY date
```

We ignore the old data, because the files can contain a very small amount data from previous years.


### IMBD: imbd

* A dataset of movies from IMBD. The dataset is stored in tsv format. Non commercial use only.