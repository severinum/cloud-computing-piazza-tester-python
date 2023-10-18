import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 10: Nick browses all the available posts on the Tech topic; at this stage, 
he can see the number of likes and dislikes for each post 
 - Mary has two likes and one dislike, and Nick has one like. 
 - There are no comments made yet.
'''

@pytest.mark.parametrize("username, email, password, roles", [
    ('Nick', 'nick@contoso.com', 'nickPa$$123', ['user'])
])
def test_TC10_ShouldValidateNumberOfActivitiesOnPosts(username, email, password, roles):
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


    ########### Get all posts for Tech topic
    # Get all posts
    url = getHost() + "/posts/topic/tech"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    responseBody = response.json();
    # Assert if 3 posts returned
    assert len(responseBody) == 3

    # Get Marys posts
    marysTechPost = []
    for post in responseBody:
        if post['owner_name'] == 'Mary':
            marysTechPost.append(post)
    assert marysTechPost != None
    assert len(marysTechPost) == 1
    assert marysTechPost[0]['like'] == 2
    assert marysTechPost[0]['dislike'] == 1
    assert marysTechPost[0]['comments'] == 0


    # Get Nick posts
    nickTechPost = []
    for post in responseBody:
        if post['owner_name'] == 'Nick':
            nickTechPost.append(post)
    assert nickTechPost != None
    assert len(nickTechPost) == 1
    assert nickTechPost[0]['like'] == 1
    assert nickTechPost[0]['dislike'] == 0
    assert nickTechPost[0]['comments'] == 0

    ####### Assert number of total comments
    # Get all posts
    url = getHost() + "/activity/comments"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    responseBody = response.json();
    assert len(responseBody) == 0