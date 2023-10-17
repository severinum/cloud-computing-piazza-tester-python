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

def test_ShouldRemoveAdminAccount_When_ValidUserId():
    ######## Login as user ########
    # Admin user was created in file test_02_add_categories.py

    url = getHost() + "/users/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': "testadmin@pythontest.com", 'password': 'test123xyz'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if response has code 200
    assert response.status_code == 200
    # Assert if response contain token
    responseBody = response.json()
    jwtToken = responseBody['token']
    assert jwtToken is not None
    # Assert if token was decoded
    jwtDecoded = jwt.decode(jwtToken, TOKEN_SECRET, algorithms=['HS512'])
    assert jwtDecoded is not None
    # Assert if token contain admin role
    userRoles = jwtDecoded['user_roles']
    userId = jwtDecoded['user_id']
    assert 'admin' in userRoles

    ######## Remove User (to maintain clean database, validate admin role for delete endpoint) ########
    url = getHost() + "/users/" + userId
    headers = {'Authorization': 'Bearer ' + jwtToken}
    response = requests.delete(url, headers=headers)
    # Assert if response has code 200
    assert response.status_code == 200
    responseBody = response.json()
    assert responseBody['message'] == 'User deleted : ' + userId

