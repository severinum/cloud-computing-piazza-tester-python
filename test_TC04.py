import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 04: Olga posts a message in the Tech topic with an expiration time (e.g. 5 minutes) using her token. 
After the end of the expiration time, the message will not accept any further user interactions (likes, dislikes, or comments). 
'''


def test_TC04_ShouldNotAddActivityOnExpiredPost_when_PostExpired():

    ############# Login as OLGA
    url = getHost() + "/users/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': 'olga@contoso.com', 'password': 'olgaPa$$123'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if response has code 200
    assert response.status_code == 200
    # Assert if response contain token
    responseBody = response.json()
    olgasToken = responseBody['token']
    assert olgasToken is not None

    # Add Olga's item
    url = getHost() + "/posts"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + olgasToken}
    payload = {
        'title': 'Olga post',
        'category': ['tech'],
        'body': 'Super cool item posted by Olga',
        'expiration_time': 0 # 0 as test can't wait 5 min, 0 is equivalemt of elapsed time
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201
    responseBody = response.json()
    olgas_expired_post_id = responseBody['_id']


    #################################################################
    ############# Login as Nestor 'Nestor', 'nestor@contoso.com', 'nestor$$123',
    url = getHost() + "/users/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': 'nestor@contoso.com', 'password': 'nestor$$123'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if response has code 200
    assert response.status_code == 200
    # Assert if response contain token
    responseBody = response.json()
    nestorsToken = responseBody['token']
    assert nestorsToken is not None

    url = getHost() + "/activity"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + olgasToken}
    payload = {
        'post_id': olgas_expired_post_id,
        'type': 'like',
        'body': '1'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 409
    responseBody = response.json()
    assert response.status_code == 409
    assert responseBody['message'] == 'Post is expired'
    
