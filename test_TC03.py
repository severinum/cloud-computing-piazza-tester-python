import pytest
import requests
import json
from configuration import *

'''
TC 03: Olga calls the API (any endpoint) without using a token. This call should be unsuccessful as the user is unauthorised.
'''


@pytest.mark.parametrize("username, email, password, roles", [
    ('Olga', 'olga@contoso.com', 'olgaPa$$123', ['user'])
])
def test_TC03_ShouldReturnStatus401_when_UserNotAuthenticated(username, email, password, roles):
    # Random endpoint. Here items
    url = getHost() + "/posts"
    headers = {'Content-Type': 'application/json'}
    payload = {'email': email, 'password': password}
    # Token not sent in header
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Assert correct response code
    assert response.status_code == 401
