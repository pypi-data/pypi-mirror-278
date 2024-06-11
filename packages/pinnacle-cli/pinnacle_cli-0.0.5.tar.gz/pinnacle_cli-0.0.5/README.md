# Pinnacle Command Line Interface
This is a command line interface for the Pinnacle API.

## Pre-requisites
- Python 3.12 or higher
- PIP: Python package manager

## Usage
1) Install the CLI using pip:
```bash
pip install pinnacle-cli
```
2) Language-specific clients can be used to define endpoints. For Python usage see the [Pinnacle Python Client README](../client-packages/pinnacle-python/README.md). 


## Commands
- `pinnacle dev`: Start the Pinnacle API server in development mode.
- `pinnacle prod` (WIP): Start the Pinnacle API server in production mode.

## Environment Variables
You can configure the CLI tool using the following environment variables:

- `PINNACLE_HOST`: The host of the Pinnacle API. Default is `localhost`.
- `PINNACLE_PORT`: The port of the Pinnacle API. Default is `8000`.
- `PINNACLE_DIRECTORY`: The directory where the Pinnacle functions are located. Default is `./pinnacle`.

## Errors and Debugging
### No matching distribution found for pinnacle-cli
If you encounter the error `No matching distribution found for pinnacle-cli`, ensure that you have the correct version of Python installed. The Pinnacle CLI requires Python 3.12 or higher.
