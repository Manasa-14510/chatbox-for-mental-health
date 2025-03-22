import openai
import streamlit as st
import os

# Set OpenAI API key
openai.api_key = "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"  # Replace with your actual API key

# Initialize chat history in session state if not already present
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        
        # Get AI response
        ai_reply = response["choices"][0]["message"]["content"]

        # Append AI response
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_reply)

    except Exception as e:
        st.error(f"⚠️ OpenAI API Error: {e}")
