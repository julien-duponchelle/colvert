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
}


@click.command()
@click.argument("dataset", type=click.Choice(["nyc_taxi"]))
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

        try:
            with urllib.request.urlopen(url) as response, open(dir / filename, 'wb') as out_file:
                # Stream the file to disk to handle large files
                chunk_size = 1024 * 1024  # 1MB chunk size
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
        except urllib.error.URLError as e:
            click.echo(f"Failed to download {url}: {e.reason}")

    click.echo(f"Downloaded {d.name} to {dir}")