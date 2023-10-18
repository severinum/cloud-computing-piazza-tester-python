import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 12: Nick and Olga comment on Mary’s post on the Tech topic in a round-robin fashion 
       (one after the other, adding at least two comments each).
'''

@pytest.mark.parametrize("username, email, password, roles", [
    ('Olga', 'olga@contoso.com', 'olgaPa$$123', ['user']),
    ('Nick', 'nick@contoso.com', 'nickPa$$123', ['user'])
])
def test_TC12_ShouldAllowToAddActivityOnOtherUsersPosts(username, email, password, roles):
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
        if post['owner_name'] == 'Mary':
            marysTechPost.append(post)
    # Assert if Mary's post in tech exists
    assert len(marysTechPost) == 1

    ########### Add comment to Mary's post
    for i in range(0,2):
        url = getHost() + "/activity"
        headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        payload = {
            'post_id': marysTechPost[0]['_id'],
            'type': 'comment',
            'body': 'Comment from ' + username
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        # Assert if add item has code 201
        assert response.status_code == 201
