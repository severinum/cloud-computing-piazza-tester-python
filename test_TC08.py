import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 08: Nick and Olga “like” Mary’ s post on the T ech topic.
'''

@pytest.mark.parametrize("username, email, password, roles", [
    ('Olga', 'olga@contoso.com', 'olgaPa$$123', ['user']),
    ('Nick', 'nick@contoso.com', 'nickPa$$123', ['user'])
])
def test_TC08_ShouldAddPost_when_UserLoggedIn(username, email, password, roles):
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


    ########### Get Mary's post in tech
    # Get all posts
    url = getHost() + "/post/topic/tech"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    responseBody = response.json();
    # Assert if 3 posts returned
    assert len(responseBody) == 3

    # Filter Mary post in tech
    marysTechPost = []
    for post in responseBody:
        if post['owner']['username'] == 'Mary':
            marysTechPost.append(post)
    # Assert if Mary's post in tech exists
    assert len(marysTechPost) == 1

    ########### Add likes to Mary's post
    url = getHost() + "/activity"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
        'post_id': marysTechPost[0]['_id'],
        'type': 'like',
        'body': '1'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    responseBody = response.json()
    assert response.status_code == 201
