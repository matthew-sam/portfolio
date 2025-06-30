from flask import Flask, request, jsonify
from urllib.parse import urlparse
from openai import OpenAI
import logging
import time
from customer_list import get_assistant_id

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
client = OpenAI()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get("message", "")

        # Detect hostname from Origin header
        origin = request.headers.get("Origin", "")
        hostname = urlparse(origin).hostname or ""
        assistant_id = get_assistant_id(hostname)

        # Step 1: Create thread
        thread = client.beta.threads.create()

        # Step 2: Add message
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Step 3: Run
        run = client.beta.threads.runs.create(
            assistant_id=assistant_id,
            thread_id=thread.id
        )

        # Step 4: Wait
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                raise Exception(f"Run failed with status: {run_status.status}")
            time.sleep(1)

        # Step 5: Get last message
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        ai_response = next(
            (m.content[0].text.value for m in reversed(messages.data) if m.role == "assistant"),
            "Sorry, I couldn't generate a response."
        )

        return jsonify({'response': ai_response, 'success': True})

    except Exception as e:
        return jsonify({'error': f'Failed to get AI response: {str(e)}', 'success': False}), 500
