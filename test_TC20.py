import pytest
import requests
import json
import jwt
from configuration import *

'''
TC 20: Nestor queries for an active post with the highest interest 
     (maximum number of likes and dislikes) in the Tech topic. 
     This should be Mary’s post.
'''

@pytest.mark.parametrize("username, email, password, roles", [
     ('Nestor', 'nestor@contoso.com', 'nestorPa$$123', ['user'])
])
def test_TC20_ShouldReturnMaryPostAsTopPostInTech(username, email, password, roles):
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


    ########### Get top post in tech topic
    url = getHost() + "/posts/top/tech"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    responseBody = response.json();

    assert responseBody['owner_name'] == 'Mary'
    
    