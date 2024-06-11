# Sensoterra

Package to retrieve Sensoterra probe data by polling the Sensoterra Customer API using async/await.

## Example code

When the email and password are always available:

```python
import time
import asyncio

from sensoterra.customerapi import CustomerApi

async def main(email, password):
	api = CustomerApi(email, password)
	api.set_language("en")

	while True:
    api.poll()

    for probe in api.probes():
        print(probe)
        for sensor in probe.sensors():
            print(sensor)
        print()

    time.sleep(900)
    print('-' * 70)

asyncio.run(main("me@example.com", "secret"))
```

Otherwise request a authentication token:

```python
from datetime import datetime

async def get_token(email, password):
  api = CustomerApi(email, password)
	api.set_language("en")

	tag = "My Application"
	scope = "READONLY"
	expiration = datetime(2038, 1, 1, 0, 0)
	token = await api.get_token(tag, scope, expiration)
```
And use this token:
```python
async def main(email, password):
  token = await get_token(email, password)

  api = CustomerApi()
	api.set_language("en")
	api.set_token(token)

	while True:
    probes = await api.poll()

    for probe in probes:
        print(probe)
        for sensor in probe.sensors():
            print(sensor)
        print()

    time.sleep(900)
    print('-' * 70)
```

## Changelog

[CHANGELOG](CHANGELOG.md)

