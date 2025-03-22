import streamlit as st
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(api_key="AIzaSyBZZ6JSwO7V6dH2I6qqLUH8_v9OiQGDO_o")

# Streamlit UI
st.title("🧠 Mental Health Chatbox")
st.write("Feel free to talk. I'm here to listen. 💙")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate AI response using OpenAI's new API structure
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    )
    ai_reply = response.choices[0].message.content

    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_reply)

