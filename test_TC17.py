import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 17: Mary dislikes Nestor’s message on the Health topic after the end of post-expiration time. This should fail.
'''

@pytest.mark.parametrize("username, email, password, roles", [
     ('Mary', 'mary@contoso.com', 'maryPa$$123', ['user'])
])
def test_TC17_ShouldNotAllowToAddCommentToExistingPostWithExpitedStatus(username, email, password, roles):
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

    # Test can't wait 5 min for Nestor post to expire, so we set it exiration status manually to Expired
    url = getHost() + "/post/"+responseBody[0]['_id']
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
         "expiration_time": 0
     }
    responsePatch = requests.patch(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 200
    assert responsePatch.status_code == 200


    ########### Get posts from Health topic again, this time with updated Post status 
    url = getHost() + "/post/topic/health"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    responseBody = response.json();
    # Assert if 3 posts returned
    assert len(responseBody) == 1
    assert responseBody[0]['owner']['username'] == 'Nestor'


    # Add activity to post
    url = getHost() + "/activity"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
          'post_id': responseBody[0]['_id'],
          'type': 'like',
          'body': '0'
     }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 409
    responseBody = response.json(); 
    assert responseBody['message'] == "Post is expired"