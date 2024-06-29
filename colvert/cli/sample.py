import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import List

import click


@dataclass
class Dataset:
    name: str
    website: str
    urls: List[str]



DATASETS = {
    "nyc_taxi":  Dataset(
        name="New York City Taxi Trip Record Data",
        website="https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page",
        urls=[
            "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
            "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet",
            "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet"
        ]
    ),
    "imbd": Dataset(
        name="IMBD",
        website="https://www.imdb.com/interfaces/",
        urls = [
            "https://datasets.imdbws.com/title.basics.tsv.gz",
        ]
    ),
}


def stream(response):
    chunk_size = 1024 * 1024  # 1MB chunk size
    while True:
        chunk = response.read(chunk_size)
        if not chunk:
            break
        yield chunk


def stream_unzip(response):
    import gzip
    with gzip.GzipFile(fileobj=response) as f:
        yield from stream(f)


@click.command()
@click.argument("dataset", type=click.Choice(list(DATASETS.keys())))
def sample(dataset) -> None:
    """
    Download a sample dataset to the tmp directory.
    """
    d = DATASETS[dataset]

    dir = Path(tempfile.gettempdir()) / dataset
    dir.mkdir(exist_ok=True)    


    for url in d.urls:
        click.echo(f"Downloading {url}...")

        filename = Path(urllib.parse.urlparse(url).path).name
        if filename.endswith(".gz"):
            reader = stream_unzip
            filename = filename[:-3]
        else:
            reader = stream

        try:
            with urllib.request.urlopen(url) as response, open(dir / filename, 'wb') as out_file:
                # Stream the file to disk to handle large files
                for chunk in reader(response):
                    out_file.write(chunk)


        except urllib.error.URLError as e:
            click.echo(f"Failed to download {url}: {e.reason}")

    click.echo(f"Downloaded {d.name} to {dir}")