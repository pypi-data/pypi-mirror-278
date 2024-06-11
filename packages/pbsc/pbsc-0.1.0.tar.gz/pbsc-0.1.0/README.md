# pbsc
High-Level API Client for Public Bike System Company

## install
```sh
pip install pbsc
```

## basic CLI usage
```sh
pbsc export-trips --base="https://example.publicbikesystem.net/operation/data" --username="jdoe" --password="2c56477e97ab8b2d180a6513" --api-key="8854c5384dd288fb8f0ad8" $PWD/trips.csv

pbsc export-stations --base="https://example.publicbikesystem.net/operation/data" --username="jdoe" --password="2c56477e97ab8b2d180a6513" --api-key="8854c5384dd288fb8f0ad8" $PWD/stations.csv

pbsc export-docks --base="https://example.publicbikesystem.net/operation/data" --username="jdoe" --password="2c56477e97ab8b2d180a6513" --api-key="8854c5384dd288fb8f0ad8" $PWD/docks.csv
```

## basic Python usage
```python
from pbsc import PBSC

client = PBSC(
    base ="https://example.publicbikesystem.net/operation/data",
    username = "jdoe",
    password = "2c56477e97ab8b2d180a6513",
    api_key = "8854c5384dd288fb8f0ad8"
)

## download csv of all trips to a file
client.export_trips("trips.csv")

## download csv of all stations to a file
client.export_stations("stations.csv")

## download csv of all docks to a file 
client.export_docks("docks.csv")
```
