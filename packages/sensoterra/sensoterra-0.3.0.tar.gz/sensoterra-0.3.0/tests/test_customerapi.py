import os
import time

import pytest

from sensoterra import customerapi


@pytest.mark.asyncio
async def test_customer_api() -> None:
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    api_url = os.environ.get("CUSTOMER_API_URL")
    api_version = os.environ.get("CUSTOMER_API_VERSION")

    assert email is not None
    assert password is not None

    api = customerapi.CustomerApi(email, password)
    if api_url is not None:
        api.api_base_url = api_url
    if api_version is not None:
        api.api_version = api_version

    probes = await api.poll()

    # We should have probes
    assert len(probes) > 0

    # Some probes should have sensors
    assert any([len(probe.sensors()) > 0 for probe in probes])
