import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 07: Nick and Olga browse all the available posts in the Tech topic; 
       three posts should be available with zero likes, zero dislikes and no comments.
'''

@pytest.mark.parametrize("username, email, password, roles", [
    ('Olga', 'olga@contoso.com', 'olgaPa$$123', ['user']),
    ('Nick', 'nick@contoso.com', 'nickPa$$123', ['user'])
])
def test_TC07_ShouldAddPost_when_UserLoggedIn(username, email, password, roles):
    ############# Login 
    url = getHost() + "/user/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': email, 'password': password}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if response has code 200
    assert response.status_code == 200
    # Assert if response contain token
    responseBody = response.json()
    token = responseBody['token']
    assert token is not None


    # Get posts by topic
    url = getHost() + "/post/topic/tech"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    responseBody = response.json();

    # Assert number od post in tech topic
    assert len(responseBody) == 3

    for post in responseBody:
        assert post['like'] == 0
        assert post['dislike'] == 0
        assert post['comments'] == 0
