import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 06: Mary posts a message in the Tech topic with an expiration time using her token.
'''

def test_TC06_ShouldAddPost_when_UserLoggedIn():

    ############# Login as Mary
    url = getHost() + "/users/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': 'mary@contoso.com', 'password': 'maryPa$$123'}
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
        'title': 'Mary post',
        'category': ['tech'],
        'body': 'Super cool item posted by Mary',
        'expiration_time': 5 
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201
    responseBody = response.json()
    postBody = responseBody['body']
    assert postBody == 'Super cool item posted by Mary'

