import requests
import json
import jwt
from random import seed
from random import random
import sys
from configuration import *

"""
    Testing if:
        - Can register new user
        - Longin as new user (plus: receiving JWT Token)
        - Remove user account (plus: if user has role admin assigned)
"""

def test_ShoulCreateAdminAccountAndLoginAsAdmin_When_AdminAuthenticated():
    # Generate random user email
    userEmail = "testadmin@pythontest.com"
    userPlainPassword = 'test123xyz'
    userUsername = 'testadmin'

    ########  Register New User (with admin role) ########
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
    # user_id: will be used to remove test user
    user_id = responseBody['_id']