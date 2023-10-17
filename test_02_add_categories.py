import requests
import json
import jwt
from random import seed
from random import random
import sys
from configuration import *

"""
    The purpose of that test is to create all required by test post categories
    It is: sport, politcs, health, tech
"""

def test_ShoulCreateAdminAccountAndLoginAsAdmin_When_AdminAuthenticated():
    ######## Log in as Admin and create categories ############
    # Admin credentials
    userEmail = "testadmin@pythontest.com"
    userPlainPassword = 'test123xyz'
    userUsername = 'testadmin'

    ########  Register admin ########
    registrationUrl = getHost() + "/users/register"
    username = userUsername
    email = userEmail
    password = userPlainPassword
    roles = ['admin']

    headers = {'Content-Type': 'application/json'}
    payload = {
        'username': username,
        'email': email,
        'password': password,
        'roles': roles
    }

    response = requests.post(registrationUrl, headers=headers, data=json.dumps(payload))
    # Assert if response has code 201
    assert response.status_code == 201
    responseBody = response.json()
    user_id = responseBody['_id']

    # Login as admin
    url = getHost() + "/users/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': email, 'password': password}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if response has code 200
    assert response.status_code == 200
    # Assert if response contain token
    responseBody = response.json()
    token = responseBody['token']
    assert token is not None

    # Add categories: sport, politcs, health, tech
    # Add topic: sport
    url = getHost() + "/topics"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
        'name': 'sport'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201

    # Add topic: politics
    payload = {
        'name': 'politics'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201

    # Add topic: health
    payload = {
        'name': 'health'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201

    # Add topic: tech
    payload = {
        'name': 'tech'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201

