import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 11: Mary likes her post on the Tech topic. This call should be unsuccessful; 
       in Piazza, a post owner cannot like their messages.
'''

@pytest.mark.parametrize("username, email, password, roles", [
    ('Mary', 'mary@contoso.com', 'maryPa$$123', ['user'])
])
def test_TC11_ShouldNotAllowToAddActivityOnOwnPost(username, email, password, roles):
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


    ########### Get all posts
    # Get all posts
    url = getHost() + "/posts/topic/tech"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    responseBody = response.json();
    # Assert if 3 posts returned
    assert len(responseBody) == 3

    

    ###################### GET MARY POST ########################
    # Filter Mary post in tech
    marysTechPost = []
    for post in responseBody:
        if post['owner']['username'] == 'Mary':
            marysTechPost.append(post)
    # Assert if Mary's post in tech exists
    assert len(marysTechPost) == 1

    ########### Add add like to Mary's own post
    url = getHost() + "/activity"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
        'post_id': marysTechPost[0]['_id'],
        'type': 'like',
        'body': '1'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 409
    assert response.status_code == 409
    responseBody = response.json();
    assert responseBody['message'] == "Can't add activities to own posts"
