import requests
import json
import random
from fastapi import status

with open(r"./../api-config.json", "r") as config:
    api_config = json.load(config)
    url = f"http://localhost:{api_config['port']}"
    api_keys = [value for _key, value in api_config["api-keys"].items()]


def test_root_success():
    response = requests.get(f"{url}", headers={"x-api-key": random.choice(api_keys)})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "hello world"}


def test_root_error_noApiKey():
    response = requests.get(f"{url}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_root_error_invalidApiKey():
    response = requests.get(f"{url}", headers={"x-api-key": "invalid"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}
