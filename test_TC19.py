import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 19: Nick browses all the expired messages on the Sports topic. These should be empty.
'''

@pytest.mark.parametrize("username, email, password, roles", [
     ('Nick', 'nick@contoso.com', 'nickPa$$123', ['user'])
])
def test_TC19_ShouldReturnZeroPosts(username, email, password, roles):
    ############# Login each user
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


    ########### Get posts from Health topic
    url = getHost() + "/posts/topic/sport"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    responseBody = response.json();
    # Assert if 3 posts returned
    assert len(responseBody) == 0
    
    