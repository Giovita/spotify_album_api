from utils.auth import get_auth_token, CLIENT_ID, CLIENT_SECRET, AUTH_URL


def test_auth_ok():
    auth_response, auth_token = get_auth_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET)
    assert auth_response == 200
    
    
def test_auth_wrong():
    wrong_client = 'some_wrong_value'
    auth_response, auth_token = get_auth_token(AUTH_URL, wrong_client, CLIENT_SECRET)
    assert auth_response == 400
    
def test_auth_token():
    auth_response, auth_token = get_auth_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET)
    assert isinstance(auth_token, str)
    