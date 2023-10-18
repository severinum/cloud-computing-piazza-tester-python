import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 13: Nick browses all the available posts in the Tech topic; 
       at this stage, he can see the number of likes and dislikes of each post and the comments made.
'''

@pytest.mark.parametrize("username, email, password, roles", [
    ('Nick', 'nick@contoso.com', 'nickPa$$123', ['user'])
])
def test_TC13_ShouldValidateNumberOfActivitiesOnPosts(username, email, password, roles):
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

    # Assert numbers of activities on posts in Tech topic
    expectedLikeCount = 3
    expectedDislikeCount = 1
    expectedCommentsCount = 4

    actualLikeCount  = 0
    actualDislikeCount = 0
    actualCommentsCount = 0
    for post in responseBody:
        actualLikeCount += post['like']
        actualDislikeCount += post['dislike']
        actualCommentsCount += post['comments']
    
    assert expectedLikeCount == actualLikeCount
    assert expectedDislikeCount == actualDislikeCount 
    assert expectedCommentsCount ==  actualCommentsCount
    