import uuid
import json

from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
import openai
import config
import redis

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(config)

# create a rotating file handler to log debug and error messages
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)

openai.api_key = config.OPENAI_API_KEY

# enable CORS
CORS(app)

# define API blueprint
api = Blueprint('api', __name__)

# create a Redis client
redis_client = redis.Redis(host='redis', port=6379)


@api.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data['input']
    session_id = data.get('session_id')

    if not session_id:
        # if no session ID is provided, generate a new one
        session_id = str(uuid.uuid4())

    # get the chat history for the current session ID from Redis
    chat_history_str = redis_client.get(session_id)
    if chat_history_str:
        # if chat history exists, deserialize it
        chat_history = json.loads(chat_history_str.decode('utf-8'))
    else:
        # if no chat history exists, create a new one
        chat_history = {"messages": [{"role": "system", "content": "You are a helpful chatbot"}]}

    user_data = chat_history

    user_data["messages"].append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model=config.OPENAI_MODEL_ENGINE,
        messages=user_data['messages'],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response["choices"][0]["message"]['content']

    user_data["messages"].append({"role": "assistant", "content": message})

    # serialize the updated chat history and store it in Redis
    redis_client.set(session_id, json.dumps(user_data))

    # log the incoming message and the response message
    app.logger.debug('Received message: %s', prompt)
    app.logger.debug('Response message: %s', message)

    return jsonify({'message': message, 'session_id': session_id})


app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    # set up the Flask app logger
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    app.run(debug=True)
