# synthientpy

A strongly typed Python client for the Synthient API.
Supports asynchronous and synchronous requests to the Synthient API.

## Installation

MacOS/Linux
```bash
pip3 install synthientpy
```
Windows
```bat
pip install synthientpy
```

## Usage

Check synthientpy/models for the available fields in the response object.

Client and AsyncClient have the following methods:

```python
api_key: str # Your private API key
default_timeout: int = DEFAULT_TIMEOUT  # Default timeout for requests, set to 5 seconds by default
proxy: str = None # Proxy URL to use for requests, set to None by default
```

### Synchronous Usage

```python
import synthientpy as synthient
client = synthient.Client(
    api_key=os.getenv("SYNTHIENT_API_KEY"),
)
token = "..."
visitor_info = client.lookup(token)
print(visitor_info)
```

### Asynchronous Usage

```python
import asyncio
import synthientpy as synthient

async def main():
    client = synthient.AsyncClient(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    token = "..."
    visitor_info = await client.lookup(token)
    print(visitor_info)

asyncio.run(main())
```
