#!/usr/bin/env python3
"""
Local development server for the AI Widget application.
Run this file to start the server locally outside of Replit.
"""

import os
from app import app

if __name__ == '__main__':
    # Set environment variables for local development
    if not os.environ.get('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print("or create a .env file with OPENAI_API_KEY=your-api-key-here")
    
    if not os.environ.get('SESSION_SECRET'):
        os.environ['SESSION_SECRET'] = 'dev-secret-key-change-in-production'
    
    print("Starting AI Widget server...")
    print("Open http://localhost:5000 to view the application")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)