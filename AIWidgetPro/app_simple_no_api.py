import osMore actions
import logging
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# Initialize OpenAI client using new SDK style
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
CORS(app, origins="*")

# Your OpenAI Assistant ID (created in platform.openai.com)
ASSISTANT_ID = "asst_zZE4Nr5XBwdulUANBvHexdEZ"

@app.route('/')
def index():
    return render_template('index.html')
# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/embed-demo')
def embed_demo():
    return render_template('embed-demo.html')
# @app.route('/embed-demo')
# def embed_demo():
#     return render_template('embed-demo.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        app.logger.info("Chat endpoint called")
        data = request.get_json()
        app.logger.info(f"Received data: {data}")

        if not data or "message" not in data:
            return jsonify({'error': 'Message is required', 'success': False}), 400

        user_message = data["message"]
        app.logger.info(f"User message: {user_message}")

        # Step 1: Create a new thread (per session)
        thread = client.beta.threads.create()
        app.logger.info(f"Thread created: {thread.id}")

        # Step 2: Add user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
        app.logger.info("Message added to thread")

        # Step 3: Run the assistant on the thread
        run = client.beta.threads.runs.create(
            assistant_id=ASSISTANT_ID,
            thread_id=thread.id
        )
        app.logger.info(f"Run started: {run.id}")

        # Step 4: Poll until the run completes
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

        # Step 5: Get messages (latest assistant response)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        ai_response = next(
            (m.content[0].text.value for m in reversed(messages.data) if m.role == "assistant"),
            "Sorry, I couldn't generate a response."
        )

        app.logger.info(f"AI response: {ai_response[:100]}...")

        return jsonify({'response': ai_response, 'success': True})

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': f'Failed to get AI response: {str(e)}', 'success': False}), 500

@app.route('/widget.js')
def widget_js():
    try:
        return app.send_static_file('widget.js'), 200, {'Content-Type': 'application/javascript'}
    except Exception as e:
        app.logger.error(f"Error serving widget.js: {str(e)}")
        return "Widget script not found", 404

@app.route('/widget.css')
def widget_css():
    try:
        return app.send_static_file('widget.css'), 200, {'Content-Type': 'text/css'}
    except Exception as e:
        app.logger.error(f"Error serving widget.css: {str(e)}")
        return "Widget stylesheet not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
