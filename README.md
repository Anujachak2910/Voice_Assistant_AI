---
title: Voice Assistant AI
emoji: 🎤
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🎙️ Multi-User AI Voice Assistant

### 🔴 **[Live Demo: Run it Now on Hugging Face Spaces!](https://huggingface.co/spaces/AnuC2910/Voice_Assistant_AI)**

A robust, real-time AI Voice Assistant built with Python, Flask, and the **Google Gemini API**. This application enables users to converse with an AI using spoken natural language, featuring dynamic session tracking, private user accounts, and seamless cloud deployment.

![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)

---

## ✨ Features

- **Push-to-Talk Architecture:** Mitigates echo-loops by securely cutting off microphone feedback while the AI synthesizes speech.
- **Multi-User Support:** Includes a secure login portal where sessions are tied to unique usernames.
- **Private Session Persistence:** Chat history is saved locally per user, allowing individuals to resume previous conversations seamlessly.
- **Web Speech API Integration:** Leverages the browser's native `SpeechRecognition` and `SpeechSynthesisUtterance` for lightweight, instantaneous voice interactions.
- **Markdown Sanitization:** Server-side pre-processing ensures AI-generated markdown (like `**bold**` or `*italic*`) is stripped to provide clean, natural-sounding Text-to-Speech output.
- **Cloud-Ready:** Completely dockerized and configured for instantaneous deployment on Hugging Face Spaces.

---

## 🛠️ Technology Stack

- **Backend:** Python, Flask, Gunicorn
- **AI Model:** Google `gemini-flash-latest` (via `google-generativeai`)
- **Frontend:** Vanilla HTML5, CSS3, JavaScript (Web Speech API)
- **Data Persistence:** Local JSON-based storage (`chats.json`)
- **Containerization:** Docker

---

## 🚀 Local Setup Instructions

Follow these steps to run the application on your local machine:

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.9 or higher
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/Anujachak2910/Voice_Assistant_AI.git
cd Voice_Assistant_AI
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a file named `.env` in the root directory and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
SECRET_KEY=your_random_flask_secret_key_here
```

### 6. Run the Application
```bash
python app.py
```
Open your web browser and navigate to `http://127.0.0.1:5000`. You will be prompted to log in with a username to begin chatting.

---

## ☁️ Deployment (Hugging Face Spaces)

This repository is pre-configured for **Hugging Face Spaces** using Docker.

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces).
2. Set the SDK to **Docker** (Blank template).
3. Under the **Settings** tab of your Space, sync this GitHub repository.
4. Still in **Settings**, navigate to **Variables and secrets** and add a new secret:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** *Your API Key*
5. The space will build automatically based on the included `Dockerfile`.

---

## 📁 Project Structure

```text
Voice_Assistant_AI/
├── app.py                 # Main Flask application and API routing
├── chat_storage.py        # Logic for reading/writing persistent user chat history
├── chats.json             # (Auto-generated) Database file storing user sessions
├── requirements.txt       # Python dependencies (Flask, gunicorn, etc.)
├── Dockerfile             # Container configuration for HF Spaces
├── .env                   # Local environment variables (Not tracked by Git)
└── templates/
    ├── index.html         # Main Chat UI, Speech Recognition/Synthesis logic
    └── login.html         # User Authentication UI
```

---

## ⚠️ Important Notes

- **Browser Compatibility:** This project heavily relies on the Web Speech API. For the best experience, please use **Google Chrome** or **Microsoft Edge**. Safari and Firefox may have limited support for native voice synthesis/recognition.
- **Network Security:** If deployed publicly without HTTPS, modern browsers may block access to the user's microphone. Hugging Face Spaces handles SSL/HTTPS out of the box.
