const WIDGET_CONFIG = {
  apiUrl: window.AI_WIDGET_API_URL || "http://localhost:5000", // fallback if not set
};

let conversationHistory = [];

function addMessage(message, isUser) {
  const container = document.getElementById("ai-widget-messages");
  const bubble = document.createElement("div");
  bubble.className = isUser ? "ai-widget-user" : "ai-widget-bot";
  bubble.innerText = message;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

function showTypingIndicator() {
  const container = document.getElementById("ai-widget-messages");
  const typing = document.createElement("div");
  typing.id = "ai-widget-typing";
  typing.className = "ai-widget-bot";
  typing.innerText = "Typing...";
  container.appendChild(typing);
  container.scrollTop = container.scrollHeight;
}

function hideTypingIndicator() {
  const typing = document.getElementById("ai-widget-typing");
  if (typing) typing.remove();
}

async function sendMessage(message) {
  try {
    showTypingIndicator();
    addMessage(message, true);
    conversationHistory.push({ role: "user", content: message });

    const response = await fetch(`${WIDGET_CONFIG.apiUrl}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history: conversationHistory }),
    });

    const data = await response.json();
    hideTypingIndicator();

    if (data.success) {
      conversationHistory.push({ role: "assistant", content: data.response });
      addMessage(data.response, false);
    } else {
      addMessage("Sorry, something went wrong.", false);
    }
  } catch (err) {
    hideTypingIndicator();
    addMessage("Error connecting to assistant.", false);
    console.error("Chat error:", err);
  }
}

function initWidget() {
  const widget = document.createElement("div");
  widget.id = "ai-widget";
  widget.innerHTML = `
    <div id="ai-widget-header">Ask a question</div>
    <div id="ai-widget-messages" class="ai-widget-scroll"></div>
    <div id="ai-widget-input-container">
      <input id="ai-widget-input" placeholder="Type a message..." />
      <button id="ai-widget-send">Send</button>
    </div>
  `;
  document.body.appendChild(widget);

  const input = document.getElementById("ai-widget-input");
  const send = document.getElementById("ai-widget-send");
  send.addEventListener("click", () => {
    const message = input.value.trim();
    if (message) {
      sendMessage(message);
      input.value = "";
    }
  });

  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") send.click();
  });
}

window.addEventListener("DOMContentLoaded", initWidget);
