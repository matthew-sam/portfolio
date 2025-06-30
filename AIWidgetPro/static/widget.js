async function sendMessage(message) {
    try {
        showTypingIndicator();

        console.log("Sending to:", WIDGET_CONFIG.apiUrl);
        console.log("Client ID:", window.AI_WIDGET_CLIENT_ID);


        const response = await fetch(`${WIDGET_CONFIG.apiUrl}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory,
                client_id: typeof window.AI_WIDGET_CLIENT_ID === "string" ? window.AI_WIDGET_CLIENT_ID : "default"
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
