# MiPasa Swarm Connector

![Tests Status](https://github.com/MiPasa/mipasa-swarm-connector/actions/workflows/tests.yaml/badge.svg) ![Integration Tests Status](https://github.com/MiPasa/mipasa-swarm-connector/actions/workflows/integration.yaml/badge.svg)

This Python library implements connecting to Swarm (BZZ) distributed storage network.

Learn more about MiPasa: https://www.mipasa.com/

Learn more about Swarm: https://www.ethswarm.org/

## Optional dependencies

- `mipasa_swarm_connector[pandas]` is required if you wish to read files as CSV or Parquet.
- `mipasa_swarm_connector[parquet]` is required if you wish to read files as Parquet. More specific versions of this dependency exist:
  - `mipasa_swarm_connector[parquet-pyarrow]`
  - `mipasa_swarm_connector[parquet-fastparquet]`

## Usage

### Simplest usage:

```python
from mipasa_swarm_connector import SwarmConnection, SwarmAPIError

try:
    content = SwarmConnection().read_file('<your_swarm_file_hash_here>')
    print(repr(content))
except SwarmAPIError as e:
    print('Failed to fetch, status: %d' % e.status_code)
```

This code will read the contents of the specified file on Swarm as bytes.

It can raise `SwarmAPIError`, which, generally, means that a file is not found (status code `404`).

### Read a file as CSV:

```python
from mipasa_swarm_connector import SwarmConnection, SwarmTypeError

try:
  dataframe = SwarmConnection().read_file('<your_swarm_file_hash_here>', as_type='csv', verify_type=True)
  print(repr(dataframe))
except SwarmTypeError as e:
  print('Expected type %s, got type %s' % (e.expected_type, e.actual_type))
```

This code will read the contents of the specified file on Swarm as a Pandas DataFrame, expecting it to be in CSV format.

`verify_type=True` can be passed (but not required) in order to check whether file's MIME type or filename matches CSV.

### Read a file as Parquet:

```python
from mipasa_swarm_connector import SwarmConnection

dataframe = SwarmConnection().read_file('<your_swarm_file_hash_here>', as_type='parquet')
print(repr(dataframe))
```

When type-checking for Parquet, two MIME types are recognized:

- `application/vnd.apache.parquet`
- `application/parquet`

### Read a file as JSON:

```python
from mipasa_swarm_connector import SwarmConnection

dataframe = SwarmConnection().read_file('<your_swarm_file_hash_here>', as_type='json')
print(repr(dataframe))
```

### Specifying custom Swarm node address

For development purposes, you can specify a custom Swarm node to work with, like so:

```python
from mipasa_swarm_connector import SwarmConnection

content = SwarmConnection('http://localhost:1633').read_file('36f0830b0ece6273a50cc0ff58c4597883e8e41ea9c8ddabb0d87d6b0ca95a1a')
print(repr(content))
```
