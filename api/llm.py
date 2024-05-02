from flask import (
    Blueprint,  request, Response, jsonify
)
from api.db.db_utils import get_db
from api.authenticate import getResourceProtector
from api.langchain_utils.openai import invokeLLM
import logging
from uuid import uuid4
from .core import limiter, get_prompt_limit_from_config

bp = Blueprint('llm', __name__)

require_auth = getResourceProtector()

# SPS: Rate limit the llm endpoints to 4 requests per second.
limiter.limit('4/second')(bp) 

@bp.route('/ping', methods=['GET'])
@require_auth(None)
def test():
    return Response(status=200)

@bp.route('/chats', methods=['GET'])
@require_auth(None)
def chats():
    """
    Get the first message of each chat the user has had.
    """
    token = require_auth.acquire_token()
    userId =  token.get('sub')

    db = get_db()
    
    chatHistoryFirstMessages = db.execute(
        """SELECT * FROM chat_history WHERE user_id = ?
        AND message_order=0
        ORDER BY created_at DESC""",
        (userId,)
    ).fetchall()
    chatHistoryFirstMessages = [cleanChatHistory(dict(row)) for row in chatHistoryFirstMessages]
    return jsonify(chatHistoryFirstMessages)

# SPS: Require_auth decorator is used to ensure that the user is authenticated before accessing the chat endpoint.
@bp.route('/chat/<chat_id>', methods=['GET', 'POST', 'DELETE'])
@bp.route('/chat/', methods=['GET', 'POST', 'DELETE'], defaults={'chat_id': None})
@limiter.limit(limit_value=get_prompt_limit_from_config, methods=['POST'], override_defaults=False, error_message='Rate limit exceeded' )
@require_auth(None)
def chat(chat_id):
    """
    Handle chat messages.
    
    GET: Get all chat messages of a conversations.
    POST: Send a message to an existing conversation or if no chat_id provided create a new conversation.
    DELETE: Delete a conversation.
    """

    token = require_auth.acquire_token()

    # SPS: Use the sub claim from the token to identify the user.
    userId =  token.get('sub')

    chatId =chat_id
    db = get_db()
    if chatId is not None:
        # SPS: Queries are parameterized.
        chatMessages = db.execute(
            """SELECT * FROM chat_history WHERE user_id = ? AND conversation_id = ?
            ORDER BY message_order ASC""",
            (userId, chatId)
        ).fetchall()
        if len(chatMessages) == 0:
            return Response(status=404)
        chatHistory = [dict(row) for row in chatMessages]
    else:
        chatHistory = []
    if request.method == 'GET':
        return jsonify([cleanChatHistory(row) for row in chatHistory])
    elif request.method == 'POST':
        prompt = request.json.get('prompt')
        if prompt is None:
            return Response(status=400, response="Prompt not provided")
        
        # SPS: Validate the prompt before sending it to the model.
        validatePromptResponse = validatePrompt(prompt)
        if validatePromptResponse is not None:
            return validatePromptResponse

        response = invokeLLM(prompt, chatHistory)
        logging.info(f"User {userId} sent prompt: {prompt}")
        logging.info(f"Response: {response}")
        if response is None:
            return Response(status=500)
        
        res = saveChat(chatHistory, userId, chatId, prompt, response)
        return jsonify(res)
    elif request.method == 'DELETE':
        if chatId is None:
            return Response(status=404)
        db.execute(
            'DELETE FROM chat_history WHERE conversation_id = ? AND user_id = ?',
            (chatId, userId)
        )
        db.commit()
        return Response(status=200)
    return Response(status=405)


def saveChat(chatHistory: list, userId: str, chatId: str | None, prompt: str, response:str ) -> dict:
    """
    Save user prompt and the response from the model to the database.
    """

    if chatId is None:
        chatId = str(uuid4())
    if len(chatHistory) == 0:
        message_order = 0
    else:
        message_order = chatHistory[-1]['message_order'] + 1


    db = get_db()
    db.execute("""
        INSERT INTO chat_history (user_id, conversation_id, message_order, from_entity, text)
        VALUES (?, ?, ?, ?, ?)
               """,
               (userId, chatId, message_order, 'User', prompt))
    message_order += 1
    db.execute("""
        INSERT INTO chat_history (user_id, conversation_id, message_order, from_entity, text)
        VALUES (?, ?, ?, ?, ?)
               """,
               (userId, chatId, message_order, 'Kev', response))
    db.commit()
    return {'chatId': chatId, 'text': response, 'from_entity': 'Kev'}


def cleanChatHistory(chatHistory: dict) -> dict:
    """
    Clean the chat history object to remove unnecessary fields.
    """
    del chatHistory['user_id']
    del chatHistory['id']
    del chatHistory['message_order']
    chatHistory['chatId'] = chatHistory['conversation_id']
    del chatHistory['conversation_id']
    return chatHistory

def validatePrompt(prompt: str) -> Response | None:
    """
    Validate the prompt to ensure it is not too long.
    """
    if len(prompt) > 10000:
        return Response(status=400, response="Prompt too long")
    return None