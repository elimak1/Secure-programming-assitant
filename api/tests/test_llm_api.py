from api.tests.token_utils import create_test_token

def test_ping(client):
    response = client.get('/ping' )
    # Not authenticated
    assert response.status_code == 401


def test_authentication_ok(client):
    token = create_test_token()
    response = client.get('/ping', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200