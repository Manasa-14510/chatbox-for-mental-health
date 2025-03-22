import streamlit as st
import openai  # Make sure you have the correct import

# Set your OpenAI API key
openai.api_key = "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"

st.title("🧠 Mental Health Chatbox")
st.write("Feel free to talk. I'm here to listen. 💙")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    )
    ai_reply = response["choices"][0]["message"]["content"]

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    with st.chat_message("assistant"):
        st.markdown(ai_reply)
