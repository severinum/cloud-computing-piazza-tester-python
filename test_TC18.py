import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 18: Nestor browses all the messages on the Health topic. There should be only one post (his own) with one comment (Mary’s).
'''

@pytest.mark.parametrize("username, email, password, roles", [
     ('Nestor', 'nestor@contoso.com', 'nestorPa$$123', ['user'])
])
def test_TC18_ShouldReturnCorrectNumberOfPosts(username, email, password, roles):
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
    url = getHost() + "/posts/topic/health"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    responseBody = response.json();
    # Assert if 3 posts returned
    assert len(responseBody) == 1
    assert responseBody[0]['owner']['username'] == 'Nestor'

    assert responseBody[0]['comments'] == 1

    assert responseBody[0]['activities'][0]['body'] == "Comment from Mary"