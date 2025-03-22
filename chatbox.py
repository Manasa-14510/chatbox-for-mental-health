import streamlit as st
import openai

# Set up OpenAI client correctly
client = openai.OpenAI(api_key="your_openai_api_key_here")

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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    )

    ai_reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    with st.chat_message("assistant"):
        st.markdown(ai_reply)
