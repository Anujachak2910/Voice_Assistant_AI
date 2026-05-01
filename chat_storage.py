import json
import os
import uuid
from datetime import datetime

CHATS_FILE = 'chats.json'

def load_chats():
    if not os.path.exists(CHATS_FILE):
        return {}
    with open(CHATS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_chats(chats):
    with open(CHATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(chats, f, indent=4)

def add_message(chat_id, username, user_input, ai_response):
    chats = load_chats()
    
    if not chat_id or chat_id not in chats:
        # Create new chat
        chat_id = str(uuid.uuid4())
        chats[chat_id] = {
            'owner': username,
            'title': user_input[:30] + '...' if len(user_input) > 30 else user_input,
            'history': [],
            'created_at': datetime.now().isoformat()
        }
    
    # Optional security: ensure the user owns the chat they are adding to
    if chats.get(chat_id, {}).get('owner') == username:
        chats[chat_id]['history'].append({
            'user': user_input,
            'ai': ai_response
        })
        chats[chat_id]['updated_at'] = datetime.now().isoformat()
        save_chats(chats)
    
    return chat_id, chats.get(chat_id, {}).get('history', [])

def get_chat_list(username):
    chats = load_chats()
    chat_list = []
    for chat_id, data in chats.items():
        if data.get('owner') == username:
            chat_list.append({
                'id': chat_id,
                'title': data.get('title', 'New Chat'),
                'updated_at': data.get('updated_at', data.get('created_at', ''))
            })
    # Sort by updated_at descending
    chat_list.sort(key=lambda x: x['updated_at'], reverse=True)
    return chat_list

def get_chat_history(chat_id, username):
    chats = load_chats()
    chat = chats.get(chat_id)
    if chat and chat.get('owner') == username:
        return chat['history']
    return []

def delete_chat(chat_id, username):
    chats = load_chats()
    chat = chats.get(chat_id)
    if chat and chat.get('owner') == username:
        del chats[chat_id]
        save_chats(chats)
        return True
    return False
