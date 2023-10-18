import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 14: Nestor posts a message in the Health topic with an expiration time using her token.
'''

@pytest.mark.parametrize("username, email, password, roles", [
    ('Nestor', 'nestor@contoso.com', 'nestorPa$$123', ['user'])
])
def test_TC14_ShouldAddPost_when_UserLoggedIn(username, email, password, roles):

    ############# Login as Mary
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

    # Add Olga's item
    url = getHost() + "/posts"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
        'title': 'Nestor post',
        'category': ['health'],
        'body': 'Super cool item posted by Nestor',
        'expiration_time': 5 
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201
    responseBody = response.json()
    postBody = responseBody['body']
    assert postBody == 'Super cool item posted by Nestor'

