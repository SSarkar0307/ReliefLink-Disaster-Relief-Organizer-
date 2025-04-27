document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const errorMessage = document.getElementById('error-message');

    // Check for dark mode preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark');
    }

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

    // Initialize
    userInput.focus();
    showWelcomeMessage();
});