import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 16: Mary posts a comment in Nestor’s message on the Health topic.
'''

@pytest.mark.parametrize("username, email, password, roles", [
     ('Mary', 'mary@contoso.com', 'maryPa$$123', ['user'])
])
def test_TC16_ShouldAllowToAddCommentToExistingPostWithLiveStatus(username, email, password, roles):
    ############# Login each user
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


    ########### Get posts from Health topic
    url = getHost() + "/post/topic/health"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    responseBody = response.json();
    # Assert if 3 posts returned
    assert len(responseBody) == 1
    assert responseBody[0]['owner']['username'] == 'Nestor'
    
    url = getHost() + "/activity"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
          'post_id': responseBody[0]['_id'],
          'type': 'comment',
          'body': 'Comment from ' + username
     }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201
    responseBody = response.json(); 
    assert responseBody['type'] == "comment"