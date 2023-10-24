import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 09: Nestor “likes” Nick’ s post and “dislikes” Mary’ s on the Tech topic.
'''

@pytest.mark.parametrize("username, email, password, roles", [
    ('Nestor', 'nestor@contoso.com', 'nestorPa$$123', ['user'])
])
def test_TC09_ShouldAddPost_when_UserLoggedIn(username, email, password, roles):
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

    ###################### NICK POST + Like ########################
    # Filter Nick post in tech
    nickTechPost = []
    for post in responseBody:
        if post['owner']['username'] == 'Nick':
            nickTechPost.append(post)
    # Assert if Nick's post in tech exists
    assert len(nickTechPost) == 1

    ########### Add like to Nick post
    url = getHost() + "/activity"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
        'post_id': nickTechPost[0]['_id'],
        'type': 'like',
        'body': '1'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201

    ###################### MARY POST + Dislike ########################
    # Filter Mary post in tech
    marysTechPost = None
    for post in responseBody:
        if post['owner']['username'] == 'Mary':
            for topic in post['category']:
                if topic == 'tech':
                    marysTechPost = post
    # Assert if Mary's post in tech exists
    assert marysTechPost != None

    ########### Add dislike to Mary's post
    url = getHost() + "/activity"
    headers = headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    payload = {
        'post_id': marysTechPost['_id'],
        'type': 'like',
        'body': '0'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert if add item has code 201
    assert response.status_code == 201
