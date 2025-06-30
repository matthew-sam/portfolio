from flask import Flask, request, jsonify
import openai
import logging
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

ASSISTANT_ID = "asst_zZE4Nr5XBwdulUANBvHexdEZ"
client = openai.OpenAI()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message", "")
    history = data.get("history", [])

    try:
        # Step 1: Create a thread
        thread = client.beta.threads.create()

        # Step 2: Add user message
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Step 3: Run assistant
        run = client.beta.threads.runs.create(
            assistant_id=ASSISTANT_ID,
            thread_id=thread.id
        )
        app.logger.info(f"Run started: {run.id}")

        # Step 4: Wait until complete
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                raise Exception("Run failed")
            time.sleep(0.5)

        # Step 5: Get response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        ai_message = messages.data[0].content[0].text.value

        app.logger.info(f"AI response: {ai_message}")
        return jsonify({"success": True, "response": ai_message})

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
