import re
import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix
import chat_storage

load_dotenv()

app = Flask(__name__)
# Fix for running behind Hugging Face's reverse proxy (needed for sessions to work)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.secret_key = os.environ.get('SECRET_KEY', 'default-dev-secret-key-123')
# Secure session cookie settings for HTTPS deployment
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

# Set your Google API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-latest")

def clean_markdown(text):
    """Strip markdown symbols from Gemini responses so stored text is plain."""
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)   # **bold** / *italic*
    text = re.sub(r'_{1,2}(.*?)_{1,2}', r'\1', text)      # __bold__ / _italic_
    text = re.sub(r'`{1,3}[^`]*`{1,3}', '', text)         # `code` / ```blocks```
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.M)    # ## headings
    text = re.sub(r'^[-*+]\s+', '', text, flags=re.M)     # - bullet points
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.M)     # 1. numbered lists
    text = re.sub(r'\n{3,}', '\n\n', text)                # excessive newlines
    return text.strip()

# Voice assistance function with enhanced topic management
def voice_assistance(username, user_input, chat_id=None):
    history = chat_storage.get_chat_history(chat_id, username) if chat_id else []
    
    history_str = ""
    if history:
        history_str = "Past Conversation:\n" + "\n".join([f"User: {item['user']}\nAI: {item['ai']}" for item in history]) + "\n"

    # Improved prompt with focus on concise and direct answers
    prompt = f"""
    You are an AI assistant in an engaging conversation with a user.
    {history_str}
    The user just asked the following question:
    '{user_input}'
    Provide a direct and informative answer, focusing on the exact details the user is asking for. Avoid unnecessary elaboration or asking follow-up questions unless essential to the user’s inquiry. Keep the response clear, concise, and to the point. If the topic is complex, briefly summarize the key aspects.
    """

    response = clean_markdown(model.generate_content(prompt).text)

    # Update conversation history in persistent storage
    new_chat_id, updated_history = chat_storage.add_message(chat_id, username, user_input, response)

    return response, new_chat_id, updated_history


# Route to render the main page
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username and username.strip():
            session['username'] = username.strip()
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/process_voice', methods=['POST'])
def process_voice():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_input = request.json.get("user_input")
    chat_id = request.json.get("chat_id")
    
    response, new_chat_id, updated_history = voice_assistance(session['username'], user_input, chat_id)

    # Return the updated conversation history and chat_id
    return jsonify({
        'response': response, 
        'conversation_history': updated_history,
        'chat_id': new_chat_id
    })


@app.route('/api/chats', methods=['GET'])
def get_chats():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(chat_storage.get_chat_list(session['username']))


@app.route('/api/chats/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({
        'chat_id': chat_id,
        'conversation_history': chat_storage.get_chat_history(chat_id, session['username'])
    })

@app.route('/api/chats/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    success = chat_storage.delete_chat(chat_id, session['username'])
    if success:
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Chat not found or unauthorized'}), 404


if __name__ == '__main__':
    app.run(debug=True)