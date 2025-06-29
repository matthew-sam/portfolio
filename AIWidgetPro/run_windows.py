#!/usr/bin/env python3
"""
Windows-compatible local development server for the AI Widget application.
Run this file to start the server locally on Windows.
"""

import os
import sys
from app_simple import app

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'flask_cors', 'openai']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall them with:")
        print("pip install Flask Flask-CORS openai")
        return False
    return True

if __name__ == '__main__':
    print("AI Widget Server - Windows Version")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check for OpenAI API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("WARNING: OPENAI_API_KEY environment variable not set!")
        print("\nTo set it on Windows:")
        print("set OPENAI_API_KEY=your-api-key-here")
        print("\nOr add it to your system environment variables.")
        print("The server will start but the AI chat won't work without the API key.")
        print()
    else:
        print("✓ OpenAI API key found")
    
    # Set session secret if not provided
    if not os.environ.get('SESSION_SECRET'):
        os.environ['SESSION_SECRET'] = 'dev-secret-key-change-in-production'
    
    print("\nStarting server...")
    print("Open http://localhost:5000 to view the application")
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nError starting server: {e}")
        input("Press Enter to exit...")