from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = "your_openai_api_key_here"

# HTML & JavaScript for frontend (Basic Chat UI)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mental Health Chatbox</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: #f4f4f4;
        }
        .chat-container {
            width: 50%;
            margin: auto;
            margin-top: 50px;
            padding: 20px;
            background: white;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
        .chat-box {
            height: 300px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            background: #e9f5ff;
            text-align: left;
        }
        .user { color: blue; text-align: right; }
        .bot { color: green; text-align: left; }
        input, button {
            margin-top: 10px;
            padding: 10px;
        }
        button { cursor: pointer; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>Mental Health Chatbox</h2>
        <div class="chat-box" id="chat-box"></div>
        <input type="text" id="user-input" placeholder="Type your message..." />
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        function appendMessage(sender, text) {
            let chatBox = document.getElementById("chat-box");
            let message = document.createElement("p");
            message.className = sender;
            message.innerHTML = "<strong>" + (sender === "user" ? "You" : "AI") + ":</strong> " + text;
            chatBox.appendChild(message);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        async function sendMessage() {
            let inputField = document.getElementById("user-input");
            let userText = inputField.value.trim();
            if (userText === "") return;

            appendMessage("user", userText);
            inputField.value = "";

            try {
                let response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: userText }),
                });

                let data = await response.json();
                appendMessage("bot", data.response);
            } catch (error) {
                console.error("Error:", error);
                appendMessage("bot", "Oops! Something went wrong.");
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # OpenAI API call to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    ai_reply = response["choices"][0]["message"]["content"]
    
    return jsonify({"response": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
