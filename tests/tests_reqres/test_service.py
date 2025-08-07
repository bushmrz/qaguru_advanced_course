import json
from jsonschema import validate

from schemas import post_users
import reqres

def test_schema_validate_from_file():
    response = reqres.post(data={"name": "morpheus", "job": "master"})

    assert response.status_code == 201

    body = response.json()

    with open("tests/tests_reqres/schema.json") as file:
        validate(body, schema=json.loads(file.read()))

def test_schema_validate_from_variable():
    response = reqres.post(data={"name": "morpheus", "job": "master"})

    assert response.status_code == 201

    body = response.json()
    validate(body, schema=post_users)


def test_job_name_from_request_returns_in_response():
    job = "master"
    name = "morpheus"

    response = reqres.post(json={"name": name, "job": job})
    body = response.json()

    assert body["name"] == name
    assert body["job"] == job


def test_get_users_returns_unique_users():
    response = reqres.get(params={"page": 2, "per_page": 4})

    ids = [element["id"] for element in response.json()["data"]]

    assert len(ids) == len(set(ids))

def test_register_success():
    email = "eve.holt@reqres.in"
    password = "pistol"

    response = reqres.register(json={"email": email, "password": password})

    assert response.status_code == 200


def test_register_negative():
    email = "error@err.er"
    response = reqres.register(json={"email": email})

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"