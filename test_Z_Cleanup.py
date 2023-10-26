import requests
import json
import jwt
from random import seed
from random import random
import sys
from configuration import *


"""
DB cleaning functions
"""

def test_ShouldEmptyTopicsCollection_When_AdminAuthenticated():
    ######## Log in as Admin and create categories ############
    # Admin credentials
    email = "testadmin@pythontest.com"
    password = 'test123xyz'
    username = 'testadmin'

    # Login as admin
    url = getHost() + "/user/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': email, 'password': password}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if response has code 200
    assert response.status_code == 200
    # Assert if response contain token
    responseBody = response.json()
    token = responseBody['token']
    assert token is not None

    # Empty topics collection
    url = getHost() + "/post/all"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 200
    assert response.status_code == 200

    # Empty topics collection
    url = getHost() + "/topic/all"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 200
    assert response.status_code == 200

    # Empty users collection
    url = getHost() + "/user/all"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 200
    assert response.status_code == 200

    # Empty activities collection
    url = getHost() + "/activity/all"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 200
    assert response.status_code == 200



