import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 01: Olga, Nick, Mary and Nestor register in the application and access the API.
'''
@pytest.mark.parametrize("username, email, password, roles", [
    ('Olga', 'olga@contoso.com', 'olgaPa$$123', ['user']),
    ('Nick', 'nick@contoso.com', 'nickPa$$123', ['user']),
    ('Mary', 'mary@contoso.com', 'maryPa$$123', ['user']),
    ('Nestor', 'nestor@contoso.com', 'nestorPa$$123', ['user'])
])
def test_TC01_should_RegisterUser_when_UserNotFound(username, email, password, roles):
        ########  Register New User ########
        url = getHost() + "/user/register"
        roles = ['user']

        headers = {'Content-Type': 'application/json'}
        payload = {
            'username': username,
            'email': email,
            'password': password,
            'roles': roles
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 201:
            responseBody = response.json()
            # user_id: will be used to remove test user
            user_id = responseBody['_id']

            ######## Login as New User (admin) ########
            url = getHost() + "/user/login"
            headers = {'Content-Type': 'application/json'}
            payload = {'email': email, 'password': password}
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
            assert 'user' in userRoles

