import requests

url = "https://reqres.in/api"
headers = {"x-api-key": "reqres-free-v1"}


def post(**kwargs):
        return requests.post(url=url + "/users", headers=headers, **kwargs)

def get(**kwargs):
        return requests.get(url=url + "/users", verify=False, **kwargs, headers=headers)

def register(**kwargs):
        return requests.post(url = url + "/register", **kwargs, headers=headers)