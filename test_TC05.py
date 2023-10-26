import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 05: Nick posts a message in the Tech topic with an expiration time using his token.
'''

def test_TC05_ShouldAddPost_when_UserLoggedIn():

    ############# Login as Nick
    url = getHost() + "/user/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': 'nick@contoso.com', 'password': 'nickPa$$123'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if response has code 200
    assert response.status_code == 200
    # Assert if response contain token
    responseBody = response.json()
    token = responseBody['token']
    assert token is not None

    # Add post
    url = getHost() + "/post"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
        'title': 'Nick post',
        'category': ['tech'],
        'body': 'Super cool item posted by Nick',
        'expiration_time': 20 
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201
    responseBody = response.json()
    postBody = responseBody['body']
    assert postBody == 'Super cool item posted by Nick'

