const WIDGET_CONFIG = {
    apiUrl: window.AI_WIDGET_API_URL || "http://localhost:5000",
};

let conversationHistory = [];

async function sendMessage(message) {
    try {
        showTypingIndicator();

        const response = await fetch(`${WIDGET_CONFIG.apiUrl}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory
            })
        });

        const data = await response.json();

        hideTypingIndicator();

        if (data.success) {
            addMessage(data.response, false);
        } else {
            addMessage('Sorry, I encountered an error. Please try again.', false);
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('Sorry, I\'m having trouble connecting. Please try again.', false);
        console.error('Widget error:', error);
    }
}
