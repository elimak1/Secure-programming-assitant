from flask import (
    Blueprint, g,  request, session, Response, jsonify
)
from api.db.db_utils import get_db
from api.authenticate import getResourceProtector
from api.langchain_utils.openai import invokeLLM
import logging

bp = Blueprint('llm', __name__)

require_auth = getResourceProtector()


@bp.route('/ping', methods=['GET'])
@require_auth(None)
def test():
    return Response(status=200)

@bp.route('/chats', methods=['GET'])
@require_auth(None)
def chats():
    token = require_auth.acquire_token()
    userId =  token.get('sub')

    db = get_db()
    
    chatHistory = db.execute(
        'SELECT * FROM chat_history WHERE user_id = ?',
        (userId,)
    ).fetchall()
    chatHistory = [dict(row) for row in chatHistory]
    return jsonify(chatHistory)

@bp.route('/chat', methods=['GET', 'POST', 'DELETE'])
@require_auth(None)
def chat():
    token = require_auth.acquire_token()
    userId =  token.get('sub')

    chatId = request.json.get('chatId')
    db = get_db()
    if chatId is not None:
        chatHistories = db.execute(
            'SELECT * FROM chat_history WHERE user_id = ? AND chatId = ?',
            (userId, chatId)
        ).fetchall()
        if len(chatHistories) == 0:
            return Response(status=404)
        chatHistory = dict(chatHistory[0])
    else:
        chatHistory = ""
    if request.method == 'GET':
        return jsonify(chatHistory)
    elif request.method == 'POST':
        prompt = request.json.get('prompt')
        response = invokeLLM(prompt)
        logging.info(f"User {userId} sent prompt: {prompt}")
        logging.info(f"Response: {response}")
        if response is None:
            return Response(status=500)
        chatHistory += f"\nUser: {prompt}\nKev: {response}"
        saveChat(chatHistory, userId, chatId)
        return jsonify({
            "chatId": chatId,
            "response": response,
            "prompt": prompt,
        })
    elif request.method == 'DELETE':
        if chatId is None:
            return Response(status=404)
        db.execute(
            'DELETE FROM chat_history WHERE chatId = ?',
            (chatId,)
        )
        db.commit()
        return Response(status=200)
    return Response(status=405)


def saveChat(text: str, userId: str, chatId: str | None ) -> None:
    print(text, userId, chatId)
    db = get_db()
    if chatId is None:
        db.execute(
            'INSERT INTO chat_history (user_id, text) VALUES (?, ?)',
            (userId, text)
        )
    else:
        db.execute(
            'UPDATE chat_history SET text = ? WHERE chatId = ? AND user_id = ?',
            (text, chatId, userId)
        )
    db.commit()