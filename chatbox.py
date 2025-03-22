import streamlit as st
import openai
import os

# Set up OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")  # For local use
# Use Streamlit Secrets for deployment
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app UI
st.title("🧠 Mental Health Chatbox")
st.write("Feel free to talk. I'm here to listen. 💙")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # OpenAI API call
        client = openai.OpenAI()  # Ensure you're using OpenAI's new client system
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        
        # Get AI response
        ai_reply = response.choices[0].message.content

        # Append AI response
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_reply)

    except openai.AuthenticationError:
        st.error("🚨 Invalid API Key! Please check your OpenAI API key.")
    except openai.OpenAIError as e:
        st.error(f"⚠️ OpenAI API Error: {e}")
