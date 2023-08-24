import requests
import json
import random
from fastapi import status

with open(r"./../api-config.json", "r") as config:
    api_config = json.load(config)
    url = f"http://localhost:{api_config['port']}"
    api_keys = [value for _key, value in api_config["api-keys"].items()]


def test_get_all_outlet_details_success():
    response = requests.get(
        f"{url}/food-outlet", headers={"x-api-key": random.choice(api_keys)}
    )

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()["outlets"]) is list

    outlets = response.json()["outlets"]

    for outlet in outlets:
        assert type(outlet["id"]) is int
        assert type(outlet["name"]) is str

        assert (outlet["location"] == None) or (type(outlet["location"]) is dict)
        if outlet["location"] is not None:
            assert type(outlet["location"]["latitude"]) is str
            assert type(outlet["location"]["longitude"]) is str

        assert (outlet["landmark"] == None) or (type(outlet["landmark"]) is str)
        assert (outlet["open_time"] == None) or (type(outlet["open_time"]) is str)
        assert (outlet["close_time"] == None) or (type(outlet["close_time"]) is str)

        assert (outlet["rating"] == None) or (type(outlet["rating"]) is dict)
        if outlet["rating"] is not None:
            assert type(outlet["rating"]["total"]) is float
            assert type(outlet["rating"]["count"]) is int

        assert (outlet["menu"] == None) or (type(outlet["menu"]) is list)
        if outlet["menu"] is not None:
            for item in outlet["menu"]:
                assert type(item["name"]) is str
                assert type(item["price"]) is int
                assert (item["description"] == None) or (
                    type(item["description"]) is str
                )

                assert (item["rating"] == None) or (type(item["rating"]) is dict)
                if item["rating"] is not None:
                    assert type(item["rating"]["total"]) is float
                    assert type(item["rating"]["count"]) is int

                assert (item["size"] == None) or (type(item["size"]) is str)
                assert (item["cal"] == None) or (type(item["cal"]) is int)
                assert (item["image"] == None) or (type(item["image"]) is str)

        assert (outlet["image"] == None) or (type(outlet["image"]) is str)


def test_get_all_outlet_details_error_noApiKey():
    response = requests.get(f"{url}/food-outlet")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_get_all_outlet_details_error_invalidApiKey():
    response = requests.get(f"{url}/food-outlet", headers={"x-api-key": "abc123"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}
