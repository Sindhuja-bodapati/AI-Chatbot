document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const logoutBtn = document.getElementById('logout-btn');
    
    // Check authentication
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }
    
    // Handle logout
    logoutBtn.addEventListener('click', function() {
        localStorage.removeItem('token');
        window.location.href = 'index.html';
    });
    
    // Handle sending messages
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage('user', message);
        userInput.value = '';
        
        // Show loading indicator
        const loadingId = 'loading-' + Date.now();
        addMessage('ai', 'Thinking...', loadingId);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Send to backend
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message and add AI response
            const loadingElement = document.getElementById(loadingId);
            if (loadingElement) {
                loadingElement.remove();
            }
            
            if (data.response) {
                addMessage('ai', data.response);
            } else {
                addMessage('ai', "Sorry, I couldn't process your request.");
            }
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            const loadingElement = document.getElementById(loadingId);
            if (loadingElement) {
                loadingElement.remove();
            }
            addMessage('ai', "An error occurred. Please try again.");
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }
    
    function addMessage(sender, text, id = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        if (id) messageDiv.id = id;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-sender">${sender === 'user' ? 'You' : 'AI Assistant'}</div>
                <div class="message-text">${text}</div>
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});