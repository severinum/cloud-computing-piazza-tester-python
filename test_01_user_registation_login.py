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

def test_ShouldLoginUser_When_UserAuthenticated():
    # Generate random user email
    seed(100)
    random_user_name = str(random())
    userEmail = random_user_name + "@pythontest.com"
    userPlainPassword = 'test123xyz'
    userUsername = random_user_name

    ########  Register New User (with admin role) ########
    registrationUrl = getHost() + "/user/register"
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

    ######## Login as New User (admin) ########
    url = getHost() + "/user/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': userEmail, 'password': userPlainPassword}
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
    assert 'admin' in userRoles

    ######## Remove New User (to maintain clean database, validate admin role for delete endpoint) ########
    url = getHost() + "/user/" + user_id
    headers = {'Authorization': 'Bearer ' + jwtToken}
    response = requests.delete(url, headers=headers)
    # Assert if response has code 200
    assert response.status_code == 200
    responseBody = response.json()
    assert responseBody['message'] == 'User deleted : ' + user_id

