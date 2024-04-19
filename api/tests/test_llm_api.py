from api.tests.token_utils import create_test_token


def test_ping(client):
    response = client.get('/ping' )
    # Not authenticated
    assert response.status_code == 401

def test_malformed_token(client):
    malformed_token = 'Bearer malformedtoken123'
    response = client.get('/ping', headers={'Authorization': malformed_token})
    assert response.status_code == 401

def test_authentication_ok(client):
    token = create_test_token()
    response = client.get('/ping', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200

def test_chats_without_authentication(client):
    response = client.get('/chats')
    assert response.status_code == 401, "Authentication must be required"

def test_chats_with_authentication(client):
    token = create_test_token(sub='123')  
    response = client.get('/chats', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert len(response.json) == 0

def test_chat_post_without_prompt(client):
    """Ensure that POST requests without a prompt are rejected."""
    token = create_test_token(sub='123')
    response = client.post('/chat/', headers={'Authorization': 'Bearer ' + token}, json={})
    print(response)
    assert response.status_code == 400
    assert 'Prompt not provided' in response.data.decode()

def test_chat_delete_nonexistent_chat(client):
    """Ensure deletion attempts on non-existing chats respond properly."""
    token = create_test_token(sub='123')
    response = client.delete('/chat/123', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 404

def test_all_chat_operations_ok(client):
    """Ensure that all chat operations work as expected."""
    token = create_test_token(sub='123')
    response = client.post('/chat/', headers={'Authorization': 'Bearer ' + token}, json={'prompt': 'Hello, how are you?'})
    assert response.status_code == 200
    assert response.json['text'] == 'Hi, how is it going?'
    chat_id = response.json['chatId']

    # Get the chat
    response = client.get(f'/chat/{chat_id}', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    # User message and llm response
    assert len(response.json) == 2

    # Get all chats
    response = client.get('/chats', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert len(response.json) == 1

    # Delete the chat
    response = client.delete(f'/chat/{chat_id}', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200


def test_chats_access_other_user_data(client):
    user_token = create_test_token(sub='123')
    response = client.post('/chat/', headers={'Authorization': 'Bearer ' + user_token}, json={'prompt': 'Hello, how are you?'})
    assert response.status_code == 200

    other_user_token = create_test_token(sub='999')  # Different user
    response = client.get('/chats', headers={'Authorization': 'Bearer ' + other_user_token})
    assert response.status_code == 200
    assert len(response.json) == 0

def test_chat_post_sql_injection(client):
    """Test resistance to SQL injection attacks via the prompt parameter."""
    token = create_test_token(sub='123')
    malicious_prompt = "test'); DROP TABLE chat_history;--"
    # Using prompt
    response = client.post('/chat/', headers={'Authorization': 'Bearer ' + token}, json={'prompt': malicious_prompt})
    assert response.status_code == 200
    # Using chat_id
    response = client.get(f'/chat/{malicious_prompt}', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 404

    # Ensure that the chat_history table still exists
    response = client.get('/chats', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200

def test_chat_post_rate_limiting(client):
    """Ensure that rate limiting is enforced for chat POST requests."""
    token = create_test_token(sub='123')
    prompt = "Hello, how are you?"

    # Rate limit is set to 4 requests per second
    for _ in range(5):
        response = client.post('/chat/', headers={'Authorization': 'Bearer ' + token}, json={'prompt': prompt})
    assert response.status_code == 429, "Should enforce rate limiting on excessive POST requests"