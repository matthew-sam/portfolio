# AI Assistant Widget - Embeddable Chat Widget

A Flask-based embeddable AI assistant widget powered by OpenAI's GPT-4o model that can be integrated into any website.

## Features

- **Easy Integration**: Add to any website with just one script tag
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **OpenAI Powered**: Uses GPT-4o for intelligent responses
- **Cross-Origin Support**: CORS enabled for embedding on any domain
- **Real-time Chat**: Instant messaging with typing indicators
- **Conversation Memory**: Maintains context throughout the conversation

## Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- OpenAI API key

### Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install Flask==3.0.0 Flask-CORS==4.0.0 openai==1.40.0 gunicorn==23.0.0
   ```

3. **Set your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```
   
   Or create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   ```

4. **Run the application**:
   ```bash
   python run_local.py
   ```

5. **Open your browser** to `http://localhost:5000`

## Project Structure

```
├── app.py              # Main Flask application
├── main.py             # Replit entry point
├── run_local.py        # Local development server
├── static/
│   ├── widget.js       # Widget JavaScript code
│   └── widget.css      # Widget styles
├── templates/
│   ├── index.html      # Demo homepage
│   └── embed-demo.html # Sample business website
└── README.md           # This file
```

## How to Embed the Widget

### Method 1: Direct Script Include

Add this script tag to any HTML page:

```html
<script src="http://your-domain.com:5000/widget.js"></script>
```

### Method 2: Custom API URL

If your API is hosted elsewhere, configure the widget:

```html
<script>
window.AI_WIDGET_API_URL = 'https://your-api-domain.com';
</script>
<script src="http://your-widget-domain.com:5000/widget.js"></script>
```

## API Endpoints

- `GET /` - Demo homepage
- `GET /embed-demo` - Sample business website with widget
- `POST /api/chat` - Chat API endpoint
- `GET /widget.js` - Widget JavaScript file
- `GET /widget.css` - Widget CSS file

## Chat API Usage

Send a POST request to `/api/chat`:

```json
{
  "message": "Hello, how can you help me?",
  "history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

Response:
```json
{
  "response": "AI assistant response",
  "success": true
}
```

## Customization

### Widget Configuration

You can customize the widget by setting these variables before loading the script:

```javascript
window.AI_WIDGET_CONFIG = {
    apiUrl: 'https://your-api.com',
    position: 'bottom-right', // or 'bottom-left'
    primaryColor: '#007bff',
    welcomeMessage: 'Hi! How can I help you today?'
};
```

### Styling

The widget supports dark mode automatically and is fully responsive. You can override styles by targeting these CSS classes:

- `.ai-widget-container` - Main container
- `.ai-widget-toggle` - Chat bubble button
- `.ai-widget-chat` - Chat window
- `.ai-widget-messages` - Messages area
- `.ai-message` - AI messages
- `.user-message` - User messages

## Deployment

### Production Deployment

1. Set environment variables:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   export SESSION_SECRET="your-session-secret"
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install Flask Flask-CORS openai gunicorn

ENV OPENAI_API_KEY=""
ENV SESSION_SECRET=""

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## Troubleshooting

### Widget doesn't appear
- Check that both `widget.js` and `widget.css` are loading without 404 errors
- Verify CORS settings if embedding on a different domain
- Check browser console for JavaScript errors

### API errors
- Ensure `OPENAI_API_KEY` environment variable is set
- Check that the API endpoint is accessible
- Verify the OpenAI API key is valid and has sufficient credits

### Local development issues
- Make sure you're running Python 3.11+
- Install all required dependencies
- Check that port 5000 is not in use by another application

## License

This is a proof of concept for demonstration purposes.

## Support

For questions or support, please refer to the documentation or contact the development team.