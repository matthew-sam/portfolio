from flask import Flask, request, jsonify
import openai
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Replace this with your actual Assistant ID
ASSISTANT_ID = "asst_zZE4Nr5XBwdulUANBvHexdEZ"

client = openai.OpenAI()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message", "")
    history = data.get("history", [])

    try:
        # Create a new thread
        thread = client.beta.threads.create()

        # Add message
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Run assistant
        run = client.beta.threads.runs.create(
            assistant_id=ASSISTANT_ID,
            thread_id=thread.id
        )

        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        ai_message = messages.data[0].content[0].text.value

        return jsonify({"success": True, "response": ai_message})

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
