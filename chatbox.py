# import openai
# import streamlit as st
# import os

# # Set OpenAI API key
# openai.api_key = "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"  # Replace with your actual API key

# # Initialize chat history in session state if not already present
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # User input
# user_input = st.chat_input("Type your message...")

# if user_input:
#     # Append user message
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     try:
#         # OpenAI API call
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
#         )
        
#         # Get AI response
#         ai_reply = response["choices"][0]["message"]["content"]

#         # Append AI response
#         st.session_state.messages.append({"role": "assistant", "content": ai_reply})

#         # Display AI response
#         with st.chat_message("assistant"):
#             st.markdown(ai_reply)

#     except Exception as e:
#         st.error(f"⚠️ OpenAI API Error: {e}")
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import sqlite3
from dotenv import load_dotenv
import os

# Load API Key from api.env
load_dotenv("api.env")  # Explicitly load api.env
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("⚠ OpenAI API Key Missing! Check your api.env file.")

app = Flask(_name_)
CORS(app)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT,
                        message TEXT,
                        response TEXT
                      )''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Mental Health Chatbot!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user = data.get("user", "Anonymous")  # Default user if not provided
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Fetch previous messages from the database
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT message, response FROM conversations WHERE user=?", (user,))
    past_conversations = cursor.fetchall()
    conn.close()

    # Format conversation history for context
    conversation_history = "\n".join([f"User: {m} \nBot: {r}" for m, r in past_conversations[-5:]])  # Last 5 messages

    # Generate AI Response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a supportive AI therapist who provides comfort."},
                {"role": "user", "content": f"Past conversations:\n{conversation_history}\n\nNew Message: {message}"}
            ]
        )
        bot_reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"error": f"OpenAI API Error: {str(e)}"}), 500

    # Store in database
