# ML Experiment Goodies

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

Helpers, handlers, callbacks and more that are nice to have when experimenting with ml models

## Setup

The most basic functionalities of this library is included in the base installation, which you have by running any of the commands below

```bash
pip install experiment-goodies
poetry add experiment-goodies
```

Geospatial utilities require some big packages, like rasterio and rio-cogeo. They are included inside the `geo` extra which you can install with one of the commands shown below.

```bash
pip install experiment-goodies[geo]
poetry add experiment-goodies -E geo
```

## Development

To develop in this repo, you will need to install some extra dependencies and make some additional configurations. Start by installing dev dependencies:

```bash
poetry install --group dev
```

Some tests depend on data managed by dvc, so you should pull files associated to this repo. Remote storage is configured to S3, so you should ensure you have the correct AWS credentials loaded in your system.

```bash
dvc pull
```
