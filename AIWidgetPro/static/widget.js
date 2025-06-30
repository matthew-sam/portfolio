(function() {
    'use strict';
    
    // Widget configuration
    const WIDGET_CONFIG = {
        apiUrl: window.AI_WIDGET_API_URL || window.location.origin,
        position: 'bottom-right',
        primaryColor: '#ff6b35',
        welcomeMessage: 'Hi! I\'m your solar assistant. Ask me about solar panels, savings, installation, or financing!'
    };
    
    // Get client ID from URL query string
    // const urlParams = new URLSearchParams(window.location.search);
    // const clientId = urlParams.get("client_id") || "default";

    // Conversation history
    let conversationHistory = [];
    let isWidgetOpen = false;
    let isTyping = false;
    
    // Create widget HTML structure
    function createWidgetHTML() {
        return `
            <div id="ai-widget-container" class="ai-widget-container">
                <!-- Widget Toggle Button -->
                <div id="ai-widget-toggle" class="ai-widget-toggle">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                
                <!-- Widget Chat Window -->
                <div id="ai-widget-chat" class="ai-widget-chat" style="display: none;">
                    <div class="ai-widget-header">
                        <h4>☀️ Solar Assistant</h4>
                        <button id="ai-widget-close" class="ai-widget-close">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                    <div id="ai-widget-messages" class="ai-widget-messages">
                        <div class="ai-message">
                            <div class="message-content">${WIDGET_CONFIG.welcomeMessage}</div>
                        </div>
                    </div>
                    <div id="ai-widget-typing" class="ai-widget-typing" style="display: none;">
                        <div class="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                    <div class="ai-widget-input">
                        <input type="text" id="ai-widget-input-field" placeholder="Type your message..." />
                        <button id="ai-widget-send" type="button">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Add message to chat
    function addMessage(content, isUser = false) {
        const messagesContainer = document.getElementById('ai-widget-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'user-message' : 'ai-message';
        messageDiv.innerHTML = `<div class="message-content">${content}</div>`;
        messagesContainer.appendChild(messageDiv);
        
        // Smooth scroll to bottom
        setTimeout(() => {
            messagesContainer.scrollTo({
                top: messagesContainer.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
        
        // Add to conversation history
        conversationHistory.push({
            role: isUser ? 'user' : 'assistant',
            content: content
        });
    }
    
    // Show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.getElementById('ai-widget-typing');
        typingDiv.style.display = 'block';
        const messagesContainer = document.getElementById('ai-widget-messages');
        setTimeout(() => {
            messagesContainer.scrollTo({
                top: messagesContainer.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
        isTyping = true;
    }
    
    // Hide typing indicator
    function hideTypingIndicator() {
        const typingDiv = document.getElementById('ai-widget-typing');
        typingDiv.style.display = 'none';
        isTyping = false;
    }
    
    // Send message to AI
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
                    // client_id: clientId
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
    
    // Toggle widget visibility
    function toggleWidget() {
        const chatWindow = document.getElementById('ai-widget-chat');
        const toggleButton = document.getElementById('ai-widget-toggle');
        
        if (isWidgetOpen) {
            chatWindow.style.display = 'none';
            toggleButton.style.transform = 'scale(1)';
            isWidgetOpen = false;
        } else {
            chatWindow.style.display = 'block';
            toggleButton.style.transform = 'scale(0.9)';
            isWidgetOpen = true;
            
            // Focus input field
            setTimeout(() => {
                document.getElementById('ai-widget-input-field').focus();
            }, 100);
        }
    }
    
    // Initialize widget
    function initWidget() {
        // Create widget container
        const widgetContainer = document.createElement('div');
        widgetContainer.innerHTML = createWidgetHTML();
        document.body.appendChild(widgetContainer);
        
        // Add event listeners
        document.getElementById('ai-widget-toggle').addEventListener('click', toggleWidget);
        document.getElementById('ai-widget-close').addEventListener('click', toggleWidget);
        
        // Send button click
        document.getElementById('ai-widget-send').addEventListener('click', function() {
            const inputField = document.getElementById('ai-widget-input-field');
            const message = inputField.value.trim();
            
            if (message && !isTyping) {
                addMessage(message, true);
                inputField.value = '';
                sendMessage(message);
            }
        });
        
        // Enter key to send
        document.getElementById('ai-widget-input-field').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const message = this.value.trim();
                
                if (message && !isTyping) {
                    addMessage(message, true);
                    this.value = '';
                    sendMessage(message);
                }
            }
        });
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        initWidget();
    }
})();
