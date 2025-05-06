from flask import Flask
from flask_restful import Api
from resources import PostListAPI, PostAPI
from django.db import connections
from google import genai
from flask import request, jsonify
import ssl
import certifi
import os

from flask_cors import CORS
os.environ['SSL_CERT_FILE'] = certifi.where()
app = Flask(__name__)
CORS(app)
api = Api(app)

# Endpoints
api.add_resource(PostListAPI, '/api/posts')
api.add_resource(PostAPI, '/api/posts/<int:post_id>')

@app.teardown_appcontext
def close_connection(exception=None):
    for conn in connections.all():
        conn.close()

@app.route('/chat/response', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    client = genai.Client(api_key="AIzaSyA4xHSj6aD6Z0HaO-7lUDLHTnQgeEf2uio")

    response = client.models.generate_content(
    model="gemini-2.0-flash", contents=user_message
)
    return jsonify({'reply': response.text})

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=False)
