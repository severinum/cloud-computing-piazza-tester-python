import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 02: Olga, Nick and Mary will use the oAuth v2 authorisation service to get their tokens.
Description: This test will log in all 3 users and check if JWT Token is returned
If so, the username will be extracted from the JWT token and compared with real username.  
'''


@pytest.mark.parametrize("username, email, password, roles", [
    ('Olga', 'olga@contoso.com', 'olgaPa$$123', ['user']),
    ('Nick', 'nick@contoso.com', 'nickPa$$123', ['user']),
    ('Mary', 'mary@contoso.com', 'maryPa$$123', ['user']),
    ('Nestor', 'nestor@contoso.com', 'nestorPa$$123', ['user'])
])
def test_TC02_ShouldReturnJwtToken_when_UserAuthenticated(username, email, password, roles):
    url = getHost() + "/users/login"
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
    user_name_from_token = jwtDecoded['user_username']
    assert user_name_from_token == username
