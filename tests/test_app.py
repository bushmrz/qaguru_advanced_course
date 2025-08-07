import random
from random import randint

import requests

base_url = "http://127.0.0.1:8000"

def test_register_user():
    username = "testuser" + str(randint)
    password = "testpassword"

    response = requests.post(url = base_url + "/register/", json={"username": username, "password": password})

    assert response.status_code == 200


def test_register_user_existing():
    requests.post(url= base_url + "/register/", json={
        "username": "existinguser",
        "password": "password"
    })

    response = requests.post(url= base_url + "/register/", json={
        "username": "existinguser",
        "password": "password"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_login_success():
    requests.post(url= base_url + "/register/", json={
        "username": "loginuser",
        "password": "mypassword"
    })

    response = requests.post(url= base_url + "/login/", json={
        "username": "loginuser",
        "password": "mypassword"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure():
    response = requests.post(url= base_url + "/login/", json={
        "username": "nonexistent",
        "password": "wrong"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"

