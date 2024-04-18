from api.tests.token_utils import create_test_token
from unittest.mock import patch
import pytest

# Mock LLM calling
@pytest.fixture
def mockLLM():
    with patch('api.langchain_utils.openai.invokeLLM') as mockinvokeLLM:
        mockinvokeLLM.return_value = "Hi, how is it going?"
        yield mockinvokeLLM

def test_ping(client):
    response = client.get('/ping' )
    # Not authenticated
    assert response.status_code == 401


def test_authentication_ok(client):
    token = create_test_token()
    response = client.get('/ping', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200