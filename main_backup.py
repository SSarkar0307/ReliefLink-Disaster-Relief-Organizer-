from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import requests
import uvicorn
import markdown2
import threading
from disaster_simulator import router as disaster_router, generate_disasters
from routes.copy import router as auth_router



app = FastAPI()
app.include_router(auth_router, prefix="/auth")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(disaster_router)

# start the simulator thread on app startup
@app.on_event("startup")
def start_simulator():
    threading.Thread(target=generate_disasters, daemon=True).start()


# Pydantic model for request body
class ChatInput(BaseModel):
    text: str

# Groq API configuration
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

@app.post("/chatbot")
async def chatbot(chat_input: ChatInput):
    user_input = chat_input.text

    if not user_input:
        return {"reply": "Please enter a message."}

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful disaster relief assistant. Always guide users with clear steps during floods, earthquakes, fires, and emergencies."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        ai_reply = data["choices"][0]["message"]["content"]

        html_reply = markdown2.markdown(ai_reply)
        return {"reply": html_reply}
    except requests.exceptions.RequestException as e:
        return {"reply": f"API request failed: {str(e)}"}
    except KeyError as e:
        return {"reply": f"Unexpected response format: {str(e)}"}
    except Exception as e:
        return {"reply": f"An error occurred: {str(e)}"}

# Serve HTML frontend
@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disaster Management Dashboard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --primary-color: #5D5CDE;
            --primary-hover: #4a49b5;
            --primary-transparent: rgba(93, 92, 222, 0.08);
            --accent-color: #FF7D7D;
            --accent-hover: #ff5c5c;
            --text-primary: #2d3748;
            --text-secondary: #4a5568;
            --bot-bubble: rgba(255, 255, 255, 0.8);
            --bot-bubble-border: rgba(226, 232, 240, 0.6);
            --user-bubble-start: #7C65FF;
            --user-bubble-end: #5D5CDE;
            --user-text: #FFFFFF;
            --error-color: #F56565;
            --success-color: #48BB78;
            --background-main: #F7FAFC;
            --background-secondary: #EDF2F7;
            --background-tertiary: #E2E8F0;
            --card-bg: rgba(255, 255, 255, 0.9);
            --border-color: rgba(226, 232, 240, 0.8);
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            --transition-default: all 0.3s ease;
        }

        .dark {
            --primary-color: #6366F1;
            --primary-hover: #818CF8;
            --primary-transparent: rgba(99, 102, 241, 0.15);
            --accent-color: #EC4899;
            --accent-hover: #F472B6;
            --text-primary: #F7FAFC;
            --text-secondary: #E2E8F0;
            --bot-bubble: rgba(51, 65, 85, 0.8);
            --bot-bubble-border: rgba(51, 65, 85, 0.4);
            --user-bubble-start: #6366F1;
            --user-bubble-end: #4F46E5;
            --user-text: #FFFFFF;
            --error-color: #F87171;
            --success-color: #4ADE80;
            --background-main: #1a202c;
            --background-secondary: #2d3748;
            --background-tertiary: #4a5568;
            --card-bg: rgba(26, 32, 44, 0.8);
            --border-color: rgba(74, 85, 104, 0.6);
        }

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(203, 213, 224, 0.8);
            border-radius: 4px;
        }

        .dark ::-webkit-scrollbar-thumb {
            background: rgba(74, 85, 104, 0.8);
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(160, 174, 192, 0.8);
        }

        .dark ::-webkit-scrollbar-thumb:hover {
            background: rgba(113, 128, 150, 0.8);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            color: var(--text-primary);
            min-height: 100vh;
            background-color: var(--background-main);
            transition: var(--transition-default);
        }

        .main-container {
            display: flex;
            flex-direction: row;
            min-height: 100vh;
            transition: var(--transition-default);
        }

        .main-container.chatbot-closed .disaster-feed-container {
            width: 100%;
        }

        .main-container.chatbot-open .disaster-feed-container {
            width: 40%;
        }

        .main-container.chatbot-open .chatbot-panel {
            width: 60%;
            left: 40%;
        }

        .disaster-feed-container {
            background: var(--card-bg);
            padding: 2rem;
            margin: 1rem;
            border-radius: 1.5rem;
            box-shadow: var(--shadow-xl);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            transition: all 0.5s ease;
            overflow-y: auto;
        }

        .disaster-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .disaster-header h1 {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .disaster-feed {
            max-height: calc(100vh - 200px);
            overflow-y: auto;
            padding-right: 1rem;
            transition: var(--transition-default);
            display: flex;
            flex-direction: column;
        }

        .disaster-item {
            background: var(--background-secondary);
            border-radius: 1rem;
            padding: 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            opacity: 0;
            transform: translateY(10px);
            animation: fadeInUp 0.4s forwards;
            transition: var(--transition-default);
        }

        .disaster-item:hover {
            background: var(--background-tertiary);
            transform: translateY(-2px);
            box-shadow: var(--shadow-sm);
        }

        .disaster-icon {
            font-size: 1.5rem;
            padding: 0.75rem;
            border-radius: 50%;
            background: var(--primary-transparent);
            color: var(--primary-color);
        }

        .disaster-details {
            flex: 1;
        }

        .disaster-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .disaster-meta {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }

        .disaster-level {
            font-size: 0.85rem;
            font-weight: 500;
            padding: 0.25rem 0.5rem;
            border-radius: 0.5rem;
        }

        .level-critical {
            background: rgba(239, 68, 68, 0.2);
            color: var(--error-color);
        }

        .level-warning {
            background: rgba(245, 158, 11, 0.2);
            color: #D97706;
        }

        .level-info {
            background: rgba(59, 130, 246, 0.2);
            color: #3B82F6;
        }

        .chatbot-toggle {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 50%;
            font-size: 1.5rem;
            cursor: pointer;
            transition: var(--transition-default);
            border: none;
            box-shadow: var(--shadow-lg);
            z-index: 1000;
        }

        .chatbot-toggle:hover {
            transform: scale(1.1);
            box-shadow: var(--shadow-xl);
        }

        .chatbot-panel {
            position: fixed;
            top: 0;
            left: 100%;
            width: 0;
            height: 100vh;
            background: var(--card-bg);
            box-shadow: var(--shadow-xl);
            transition: left 0.5s ease, width 0.5s ease;
            z-index: 999;
            display: flex;
            flex-direction: column;
            opacity: 0;
        }

        .chatbot-panel.open {
            opacity: 1;
        }

        .chatbot-header {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
            color: white;
            padding: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: var(--shadow);
        }

        .chatbot-header h2 {
            font-size: 1.2rem;
            font-weight: 600;
        }

        .close-chatbot {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            color: white;
            cursor: pointer;
            transition: var(--transition-default);
        }

        .close-chatbot:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }

        .chat-messages {
            flex: 1;
            padding: 1.5rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            scroll-behavior: smooth;
            background-color: var(--background-main);
        }

        .message-container {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            max-width: 85%;
            opacity: 0;
            transform: translateY(10px);
            animation: fadeInUp 0.4s forwards;
        }

        .message-container.user {
            align-self: flex-end;
        }

        .message-container.bot {
            align-self: flex-start;
        }

        .message-bubble {
            position: relative;
            display: flex;
            flex-direction: column;
        }

        .message-header {
            display: flex;
            align-items: center;
            margin-bottom: 0.25rem;
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        .user .message-header {
            justify-content: flex-end;
        }

        .message {
            padding: 0.9rem 1.2rem;
            border-radius: 1.5rem;
            font-size: 0.95rem;
            line-height: 1.6;
            position: relative;
            z-index: 1;
            overflow-wrap: break-word;
            transition: var(--transition-default);
        }

        .message-container.bot .message {
            background-color: var(--bot-bubble);
            border: 1px solid var(--bot-bubble-border);
            color: var(--text-primary);
            border-bottom-left-radius: 0.3rem;
            box-shadow: var(--shadow-sm);
            backdrop-filter: blur(10px);
        }

        .message-container.user .message {
            background: linear-gradient(135deg, var(--user-bubble-start), var(--user-bubble-end));
            color: var(--user-text);
            border-bottom-right-radius: 0.3rem;
            box-shadow: var(--shadow);
        }

        .timestamp-wrapper {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.3rem;
            font-size: 0.7rem;
            color: var(--text-secondary);
        }

        .user .timestamp-wrapper {
            justify-content: flex-end;
        }

        .message-actions {
            opacity: 0;
            transition: var(--transition-default);
            display: flex;
            gap: 0.3rem;
        }

        .message-container:hover .message-actions {
            opacity: 1;
        }

        .action-button {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 2px;
            border-radius: 4px;
            font-size: 0.7rem;
            transition: var(--transition-default);
        }

        .action-button:hover {
            color: var(--primary-color);
            background-color: var(--primary-transparent);
        }

        .bot-message p {
            margin-bottom: 0.75rem;
        }

        .bot-message p:last-child {
            margin-bottom: 0;
        }

        .bot-message ul, .bot-message ol {
            margin-left: 1.5rem;
            margin-bottom: 0.75rem;
        }

        .bot-message li {
            margin-bottom: 0.25rem;
        }

        .bot-message code {
            background-color: rgba(0, 0, 0, 0.05);
            padding: 0.15rem 0.3rem;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
            font-size: 0.9em;
        }

        .dark .bot-message code {
            background-color: rgba(0, 0, 0, 0.2);
        }

        .bot-message pre {
            background-color: rgba(0, 0, 0, 0.05);
            padding: 0.75rem;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 0.75rem;
        }

        .dark .bot-message pre {
            background-color: rgba(0, 0, 0, 0.2);
        }

        .bot-message a {
            color: var(--primary-color);
            text-decoration: none;
            border-bottom: 1px dotted var(--primary-color);
            transition: var(--transition-default);
        }

        .bot-message a:hover {
            border-bottom: 1px solid var(--primary-color);
        }

        .typing-indicator {
            display: flex;
            align-self: flex-start;
            padding: 1.2rem 1.5rem;
            background-color: var(--bot-bubble);
            border: 1px solid var(--bot-bubble-border);
            border-radius: 1.5rem;
            border-bottom-left-radius: 0.3rem;
            margin-top: 0.5rem;
            animation: fadeIn 0.3s forwards;
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow-sm);
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            background-color: var(--primary-color);
            border-radius: 50%;
            margin: 0 3px;
            opacity: 0.7;
            animation: typingAnimation 1.4s infinite ease-in-out;
        }

        .typing-dot:nth-child(1) { animation-delay: 0s; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        .chat-input-container {
            padding: 1.25rem 1.5rem;
            border-top: 1px solid var(--border-color);
            background-color: var(--card-bg);
            display: flex;
            flex-direction: column;
            z-index: 10;
            box-shadow: var(--shadow);
            backdrop-filter: blur(16px);
            transition: var(--transition-default);
        }

        .input-wrapper {
            display: flex;
            align-items: flex-end;
            background-color: var(--background-main);
            border: 1px solid var(--border-color);
            border-radius: 1.5rem;
            padding: 0.5rem 0.75rem;
            transition: var(--transition-default);
        }

        .input-wrapper:focus-within {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px var(--primary-transparent);
        }

        .input-icons {
            display: flex;
            align-items: center;
            padding: 0.5rem;
        }

        .input-icon {
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-right: 0.5rem;
            cursor: pointer;
            padding: 0.3rem;
            border-radius: 50%;
            transition: var(--transition-default);
        }

        .input-icon:hover {
            color: var(--primary-color);
            background-color: var(--primary-transparent);
        }

        #user-input {
            flex: 1;
            padding: 0.75rem 0.5rem;
            border: none;
            background: transparent;
            outline: none;
            font-size: 1rem;
            line-height: 1.5;
            resize: none;
            max-height: 150px;
            font-family: inherit;
            color: var(--text-primary);
            transition: var(--transition-default);
        }

        #send-button {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
            color: white;
            border: none;
            cursor: pointer;
            transition: var(--transition-default);
            flex-shrink: 0;
            box-shadow: var(--shadow-sm);
            margin-left: 0.5rem;
        }

        #send-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(93, 92, 222, 0.4);
        }

        #send-button:active {
            transform: translateY(0);
        }

        #send-button:disabled {
            background: var(--text-secondary);
            cursor: not-allowed;
            box-shadow: none;
        }

        .helper-text {
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 0.75rem;
            text-align: center;
            transition: var(--transition-default);
        }

        .error-message {
            background-color: rgba(239, 68, 68, 0.1);
            color: var(--error-color);
            padding: 0.75rem 1rem;
            border-radius: 10px;
            margin-top: 0.75rem;
            font-size: 0.85rem;
            display: none;
            animation: fadeIn 0.3s ease;
            border: 1px solid rgba(239, 68, 68, 0.2);
            transition: var(--transition-default);
        }

        .dark .error-message {
            background-color: rgba(239, 68, 68, 0.2);
        }

        .quick-actions {
            padding: 0.75rem 1rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
            border-bottom: 1px solid var(--border-color);
            background-color: var(--card-bg);
        }

        .quick-btn {
            padding: 0.5rem 1rem;
            border-radius: 1.5rem;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-default);
            border: none;
            color: white;
            box-shadow: var(--shadow-sm);
            white-space: nowrap;
        }

        .quick-btn:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow);
        }

        .quick-btn:active {
            transform: translateY(0);
        }

        .shelter-btn { background-color: #3B82F6; }
        .water-btn { background-color: #10B981; }
        .earthquake-btn { background-color: #F59E0B; }
        .emergency-btn { background-color: #EF4444; }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        @keyframes typingAnimation {
            0%, 60%, 100% {
                transform: translateY(0);
            }
            30% {
                transform: translateY(-4px);
            }
        }

        @media (max-width: 768px) {
            .main-container {
                flex-direction: column;
            }

            .main-container.chatbot-open .disaster-feed-container {
                width: 100%;
                height: 30vh;
            }

            .main-container.chatbot-open .chatbot-panel {
                width: 100%;
                left: 0;
                top: 30vh;
            }

            .disaster-feed-container {
                margin: 0;
                border-radius: 0;
            }

            .chatbot-panel {
                max-width: 100%;
            }
        }

        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border-width: 0;
        }
    </style>
</head>
<body>
    <div class="main-container chatbot-closed" id="main-container">
        <div class="disaster-feed-container" id="disaster-feed-container">
            <div class="disaster-header">
                <h1>Live Disaster Feed</h1>
            </div>
            <div class="disaster-feed" id="disaster-feed">
                <!-- Disaster events will appear here -->
            </div>
        </div>
        <div class="chatbot-panel" id="chatbot-panel">
            <div class="chatbot-header">
                <h2>AI Assistant</h2>
                <button class="close-chatbot" id="close-chatbot" aria-label="Close chatbot">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="quick-actions">
                <button class="quick-btn shelter-btn" data-question="Where is the nearest shelter?">
                    <i class="fas fa-home"></i> Shelter
                </button>
                <button class="quick-btn water-btn" data-question="How can I get clean drinking water?">
                    <i class="fas fa-tint"></i> Water
                </button>
                <button class="quick-btn earthquake-btn" data-question="What to do in case of an earthquake?">
                    <i class="fas fa-mountain"></i> Earthquake
                </button>
                <button class="quick-btn emergency-btn" data-question="How to contact emergency services?">
                    <i class="fas fa-ambulance"></i> Emergency
                </button>
            </div>
            <div class="chat-messages" id="chat-messages">
                <!-- Messages will appear here -->
            </div>
            <div class="chat-input-container">
                <div class="input-wrapper">
                    <div class="input-icons">
                        <i class="fas fa-microphone input-icon" aria-label="Voice input"></i>
                        <i class="fas fa-paperclip input-icon" aria-label="Attach file"></i>
                    </div>
                    <textarea 
                        id="user-input" 
                        placeholder="Type your message..." 
                        rows="1"
                        aria-label="Message input field"></textarea>
                    <button id="send-button" aria-label="Send message">
                        <i class="fas fa-paper-plane"></i>
                        <span class="sr-only">Send</span>
                    </button>
                </div>
                <div class="helper-text">Press Enter to send, Shift+Enter for new line</div>
                <div class="error-message" id="error-message"></div>
            </div>
        </div>
    </div>

    <button class="chatbot-toggle" id="open-chatbot" aria-label="Chat with Assistant">
        <i class="fas fa-comment-dots"></i>
    </button>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const chatMessages = document.getElementById('chat-messages');
            const userInput = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');
            const errorMessage = document.getElementById('error-message');
            const openChatbot = document.getElementById('open-chatbot');
            const closeChatbot = document.getElementById('close-chatbot');
            const chatbotPanel = document.getElementById('chatbot-panel');
            const disasterFeedContainer = document.getElementById('disaster-feed-container');
            const disasterFeed = document.getElementById('disaster-feed');
            const mainContainer = document.getElementById('main-container');

            // Check for dark mode preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.documentElement.classList.add('dark');
            }

            // Toggle chatbot panel
            openChatbot.addEventListener('click', function() {
                chatbotPanel.classList.add('open');
                mainContainer.classList.remove('chatbot-closed');
                mainContainer.classList.add('chatbot-open');
            });

            closeChatbot.addEventListener('click', function() {
                chatbotPanel.classList.remove('open');
                mainContainer.classList.remove('chatbot-open');
                mainContainer.classList.add('chatbot-closed');
            });

            // Auto-resize textarea
            function autoResizeTextarea(element) {
                element.style.height = 'auto';
                element.style.height = (element.scrollHeight < 150) ? element.scrollHeight + 'px' : '150px';
            }

            userInput.addEventListener('input', function() {
                autoResizeTextarea(this);
            });

            // Reset textarea height
            function resetTextarea() {
                userInput.value = '';
                userInput.style.height = 'auto';
            }

            // Format timestamps
            function formatTimestamp(timestamp) {
                const date = new Date(timestamp * 1000);
                return date.toLocaleString();
            }

            // Add a message to the chat
            function addMessage(content, isUser) {
                const messageContainer = document.createElement('div');
                messageContainer.classList.add('message-container');
                messageContainer.classList.add(isUser ? 'user' : 'bot');

                const timestamp = formatTimestamp(Date.now());

                if (isUser) {
                    messageContainer.innerHTML = `
                        <div class="message-bubble">
                            <div class="message-header">
                                <span>You</span>
                            </div>
                            <div class="message">${content}</div>
                            <div class="timestamp-wrapper">
                                <div class="message-actions">
                                    <button class="action-button"><i class="fas fa-copy"></i> Copy</button>
                                </div>
                                <span class="timestamp">${timestamp}</span>
                            </div>
                        </div>
                    `;
                } else {
                    const parsedContent = marked.parse(content);
                    messageContainer.innerHTML = `
                        <div class="message-bubble">
                            <div class="message-header">
                                <span>AI Assistant</span>
                            </div>
                            <div class="message bot-message">${parsedContent}</div>
                            <div class="timestamp-wrapper">
                                <div class="message-actions">
                                    <button class="action-button"><i class="fas fa-copy"></i> Copy</button>
                                    <button class="action-button"><i class="fas fa-thumbs-up"></i></button>
                                    <button class="action-button"><i class="fas fa-thumbs-down"></i></button>
                                </div>
                                <span class="timestamp">${timestamp}</span>
                            </div>
                        </div>
                    `;
                }

                chatMessages.appendChild(messageContainer);
                scrollToBottom();
                addCopyButtonListeners(messageContainer, content, isUser);
            }

            // Add event listeners to copy buttons
            function addCopyButtonListeners(container, content, isUser) {
                const copyButtons = container.querySelectorAll('.action-button:first-child');
                copyButtons.forEach(button => {
                    button.addEventListener('click', function() {
                        const textToCopy = isUser ? content : content;
                        navigator.clipboard.writeText(textToCopy).then(() => {
                            const originalHTML = button.innerHTML;
                            button.innerHTML = '<i class="fas fa-check"></i> Copied';
                            setTimeout(() => {
                                button.innerHTML = originalHTML;
                            }, 2000);
                        });
                    });
                });
            }

            // Scroll to bottom of chat
            function scrollToBottom() {
                setTimeout(() => {
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 100);
            }

            // Show typing indicator
            function showTypingIndicator() {
                const typingDiv = document.createElement('div');
                typingDiv.classList.add('typing-indicator');
                typingDiv.id = 'typing-indicator';
                typingDiv.innerHTML = `
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                `;
                chatMessages.appendChild(typingDiv);
                scrollToBottom();
            }

            // Hide typing indicator
            function hideTypingIndicator() {
                const typingIndicator = document.getElementById('typing-indicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
            }

            // Show error message
            function showError(message) {
                errorMessage.textContent = message;
                errorMessage.style.display = 'block';
                setTimeout(() => {
                    errorMessage.style.display = 'none';
                }, 5000);
            }

            // Send message to API
            async function sendMessage(optionalMessage = null) {
                const message = optionalMessage || userInput.value.trim();
                if (!message) return;

                addMessage(message, true);
                resetTextarea();
                sendButton.disabled = true;

                showTypingIndicator();

                try {
                    const response = await fetch('/chatbot', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: message }),
                    });

                    if (!response.ok) {
                        throw new Error(`Request failed with status ${response.status}`);
                    }

                    const data = await response.json();
                    hideTypingIndicator();
                    addMessage(data.reply, false);
                } catch (error) {
                    hideTypingIndicator();
                    addMessage("Sorry, I encountered a problem. Please try again later.", false);
                    showError(`Error: ${error.message}`);
                    console.error('Error:', error);
                } finally {
                    sendButton.disabled = false;
                    userInput.focus();
                }
            }

            // Send quick question
            function sendQuickQuestion(question) {
                const buttons = document.querySelectorAll('.quick-btn');
                buttons.forEach(btn => btn.disabled = true);

                const clickedBtn = event.target.closest('.quick-btn');
                const originalHTML = clickedBtn.innerHTML;

                clickedBtn.innerHTML = '<i class="fas fa-spinner fa-pulse"></i> ' + clickedBtn.textContent.trim();

                setTimeout(() => {
                    sendMessage(question);
                    setTimeout(() => {
                        clickedBtn.innerHTML = originalHTML;
                        buttons.forEach(btn => btn.disabled = false);
                    }, 300);
                }, 300);
            }

            // Add event listeners for quick buttons
            document.querySelectorAll('.quick-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const question = this.getAttribute('data-question');
                    sendQuickQuestion(question);
                });
            });

            // Event listeners
            sendButton.addEventListener('click', sendMessage);
            userInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            // Handle microphone and paperclip icons
            document.querySelectorAll('.input-icon').forEach(icon => {
                icon.addEventListener('click', function() {
                    icon.style.color = 'var(--primary-color)';
                    setTimeout(() => {
                        icon.style.color = 'var(--text-secondary)';
                    }, 500);
                });
            });

            // Welcome message
            function showWelcomeMessage() {
                setTimeout(() => {
                    showTypingIndicator();
                    setTimeout(() => {
                        hideTypingIndicator();
                        addMessage("Hello! 👋 I'm your AI assistant. How can I help you with disaster relief today?", false);
                    }, 1500);
                }, 500);
            }

            // Fetch and render disaster feed
            async function fetchDisasterFeed() {
                try {
                    const res = await fetch('/alerts');
                    if (!res.ok) throw new Error('Network response was not ok');
                    const data = await res.json();
                    disasterFeed.innerHTML = '';
                    data.forEach(alert => {
                        const icon = alert.disaster.toLowerCase().includes('flood') ? 'fa-water' :
                                    alert.disaster.toLowerCase().includes('earthquake') ? 'fa-mountain' :
                                    alert.disaster.toLowerCase().includes('fire') ? 'fa-fire' : 'fa-exclamation-triangle';
                        const levelClass = alert.level >= 7 ? 'level-critical' :
                                         alert.level >= 5 ? 'level-warning' : 'level-info';
                        const levelText = alert.level >= 7 ? 'Critical' :
                                         alert.level >= 5 ? 'Warning' : 'Info';

                        const feedItem = document.createElement('div');
                        feedItem.className = 'disaster-item';
                        feedItem.innerHTML = `
                            <i class="fas ${icon} disaster-icon"></i>
                            <div class="disaster-details">
                                <div class="disaster-title">${alert.disaster.toUpperCase()} at ${alert.location}</div>
                                <div class="disaster-meta">${formatTimestamp(alert.timestamp)}</div>
                            </div>
                            <span class="disaster-level ${levelClass}">Lvl ${alert.level} (${levelText})</span>
                        `;
                        disasterFeed.appendChild(feedItem);
                    });
                    // Scroll to the bottom to show the latest item
                    disasterFeed.scrollTop = disasterFeed.scrollHeight;
                } catch (e) {
                    console.error('fetchDisasterFeed error', e);
                    disasterFeed.innerHTML = '<div class="text-center text-error-color">Failed to load disaster feed.</div>';
                }
            }

            // Initialize
            userInput.focus();
            showWelcomeMessage();
            setInterval(fetchDisasterFeed, 5000);
            fetchDisasterFeed();
        });
    </script>
</body>
</html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)