import os
import logging
import openai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Enable CORS for cross-origin requests (needed for embeddable widget)
CORS(app, origins="*")

# Set up OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

app.logger.info("OpenAI legacy client initialized (API key pulled from env)")

@app.route('/')
def index():
    """Main demonstration page showing the widget in action"""
    return render_template('index.html')

@app.route('/embed-demo')
def embed_demo():
    """Demo page showing how the widget looks when embedded on another site"""
    return render_template('embed-demo.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint to handle chat messages and return AI responses"""
    try:
        app.logger.info("Chat endpoint called")
        
        data = request.get_json()
        app.logger.info(f"Received data: {data}")
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required', 'success': False}), 400
        
        user_message = data['message']
        conversation_history = data.get('history', [])
        
        app.logger.info(f"Processing message: {user_message}")
        
        # Build conversation context - using the same format as the working test
        messages = []
        
        # Add system message for the AI assistant
        messages.append({
            "role": "system",
            "content": "You are a knowledgeable solar energy consultant embedded on a solar company website. Help customers understand solar panels, calculate potential savings, explain installation processes, and provide information about financing options. Be friendly, professional, and focus on the benefits of solar energy. Answer questions about:\n\n- Solar panel costs and savings calculations\n- System sizing based on energy usage\n- Installation timeline and process\n- Financing options and tax incentives\n- Equipment warranties and maintenance\n- Environmental benefits\n\nIf asked about specific pricing, encourage them to get a personalized quote. Always be helpful and encouraging about solar adoption."
        })
        
        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            messages.append({
                "role": msg.get('role', 'user'),
                "content": msg.get('content', '')
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        app.logger.info("Calling OpenAI API...")
        
        # Use legacy OpenAI API call (same style as your working test script)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        app.logger.info(f"OpenAI response received: {ai_response[:100]}...")
        
        return jsonify({
            'response': ai_response,
            'success': True
        })
        
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': f'Failed to get AI response: {str(e)}',
            'success': False
        }), 500

@app.route('/widget.js')
def widget_js():
    """Serve the widget JavaScript file"""
    try:
        return app.send_static_file('widget.js'), 200, {'Content-Type': 'application/javascript'}
    except Exception as e:
        app.logger.error(f"Error serving widget.js: {str(e)}")
        return "Widget script not found", 404

@app.route('/widget.css')
def widget_css():
    """Serve the widget CSS file"""
    try:
        return app.send_static_file('widget.css'), 200, {'Content-Type': 'text/css'}
    except Exception as e:
        app.logger.error(f"Error serving widget.css: {str(e)}")
        return "Widget stylesheet not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
