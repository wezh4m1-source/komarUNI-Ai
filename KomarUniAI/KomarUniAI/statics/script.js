// ========================================
// GLOBAL VARIABLES
// ========================================

let chatHistory = [];
let allSources = [];
let messagesContainer = document.getElementById('chatMessages');

// ========================================
// INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Komar Uni AI initialized');
    initializeEventListeners();
    loadChatHistory();
});

function initializeEventListeners() {
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.addEventListener('keypress', handleKeyPress);
    }
}

// ========================================
// SEND MESSAGE
// ========================================

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (!message) {
        showToast('Please enter a message', 'warning');
        return;
    }

    // Add user message to chat
    addMessageToChat(message, 'user');
    userInput.value = '';
    userInput.focus();

    // Show loading spinner
    showLoading(true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Add AI message to chat
        addMessageToChat(data.response, 'ai');

        // Display sources if available
        if (data.has_research && data.sources.length > 0) {
            displaySources(data.sources);
        }

        // Update history
        updateHistory();

        // Play notification sound if enabled
        if (document.getElementById('soundNotification').checked) {
            playNotificationSound();
        }

    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('Sorry, I encountered an error. Please try again.', 'ai');
        showToast('Error sending message', 'error');
    } finally {
        showLoading(false);
    }
}

// ========================================
// ADD MESSAGE TO CHAT
// ========================================

function addMessageToChat(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = sender === 'user' ? '👤' : '🤖';
    const name = sender === 'user' ? 'You' : 'Komar Uni AI';

    const timestamp = document.getElementById('showTimestamps').checked 
        ? ` <small style="opacity: 0.7;">${new Date().toLocaleTimeString()}</small>`
        : '';

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <strong>${name}:</strong>${timestamp}
            <p style="margin: 0.5rem 0 0 0; white-space: pre-wrap; word-wrap: break-word;">${escapeHtml(message)}</p>
        </div>
    `;

    messagesContainer.appendChild(messageDiv);

    // Auto-scroll if enabled
    if (document.getElementById('autoScroll').checked) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// ========================================
// HANDLE KEYBOARD EVENTS
// ========================================

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ========================================
// QUICK SEARCH
// ========================================

function quickSearch(topic) {
    const queries = {
        'python': 'Tell me about Python programming',
        'ai': 'What is artificial intelligence?',
        'kust': 'Tell me about KUST university',
        'web': 'How do I start with web development?',
        'javascript': 'Explain JavaScript for beginners'
    };

    const userInput = document.getElementById('userInput');
    userInput.value = queries[topic] || topic;
    userInput.focus();
    sendMessage();
}

// ========================================
// ADD TOPIC FROM SIDEBAR
// ========================================

function addTopic(topic) {
    const userInput = document.getElementById('userInput');
    userInput.value = topic;
    userInput.focus();
    sendMessage();
}

// ========================================
// DISPLAY SOURCES
// ========================================

function displaySources(sources) {
    const sourcesContainer = document.getElementById('sourcesContainer');
    const sourcesList = document.getElementById('sourcesList');

    const sourcesHtml = sources.map(source => `
        <div class="source-item">
            <strong>${source.title || 'Source'}</strong>
            ${source.link ? `<br><a href="${source.link}" target="_blank">Read more →</a>` : ''}
            <br><small>Source: ${source.source || 'Verified'}</small>
        </div>
    `).join('');

    sourcesList.innerHTML = sourcesHtml;
    sourcesContainer.style.display = 'block';

    allSources = [...allSources, ...sources];
}

// ========================================
// TOGGLE SOURCES
// ========================================

function toggleSources() {
    const content = document.querySelector('.sources-content');
    if (content.style.display === 'none') {
        content.style.display = 'grid';
    } else {
        content.style.display = 'none';
    }
}

// ========================================
// CLEAR HISTORY
// ========================================

async function clearHistory() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        try {
            const response = await fetch('/api/clear', { method: 'POST' });
            const data = await response.json();

            if (data.status === 'cleared') {
                messagesContainer.innerHTML = `
                    <div class="message ai-message">
                        <div class="message-avatar">🤖</div>
                        <div class="message-content">
                            <strong>Komar Uni AI:</strong>
                            <p style="margin: 0.5rem 0 0 0;">Chat cleared! How can I help you now? 🚀</p>
                        </div>
                    </div>
                `;
                chatHistory = [];
                allSources = [];
                updateHistory();
                showToast('Chat history cleared', 'success');
            }
        } catch (error) {
            console.error('Error clearing history:', error);
            showToast('Error clearing history', 'error');
        }
    }
}

// ========================================
// DOWNLOAD HISTORY
// ========================================

function downloadHistory() {
    if (chatHistory.length === 0) {
        showToast('No history to download', 'warning');
        return;
    }

    const dataStr = JSON.stringify(chatHistory, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement('a');
    link.href = url;
    link.download = `komar-chat-history-${new Date().getTime()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showToast('History downloaded!', 'success');
}

// ========================================
// UPDATE HISTORY SIDEBAR
// ========================================

async function updateHistory() {
    try {
        const response = await fetch('/api/history');
        const history = await response.json();
        chatHistory = history;

        const historyList = document.getElementById('historyList');

        if (history.length === 0) {
            historyList.innerHTML = '<p class="empty-state">No messages yet</p>';
            return;
        }

        historyList.innerHTML = history.map((msg, index) => `
            <div class="history-item" title="${msg.user}">
                <strong>[${index + 1}]</strong> ${msg.user.substring(0, 40)}...
            </div>
        `).join('');

    } catch (error) {
        console.error('Error updating history:', error);
    }
}

// ========================================
// LOAD CHAT HISTORY ON PAGE LOAD
// ========================================

function loadChatHistory() {
    updateHistory();
}

// ========================================
// SCROLL TO CHAT
// ========================================

function scrollToChat() {
    const chatSection = document.getElementById('chat');
    if (chatSection) {
        chatSection.scrollIntoView({ behavior: 'smooth' });
        document.getElementById('userInput').focus();
    }
}

// ========================================
// HANDLE CONTACT FORM
// ========================================

function handleContactForm(event) {
    event.preventDefault();
    showToast('Thank you for your message! We will get back to you soon.', 'success');
    event.target.reset();
}

// ========================================
// TOGGLE MENU
// ========================================

function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks.style.display === 'flex') {
        navLinks.style.display = 'none';
    } else {
        navLinks.style.display = 'flex';
    }
}

// ========================================
// LOADING SPINNER
// ========================================

function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (show) {
        spinner.style.display = 'flex';
    } else {
        spinner.style.display = 'none';
    }
}

// ========================================
// TOAST NOTIFICATION
// ========================================

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show`;

    // Add type styling
    if (type === 'error') {
        toast.style.background = '#dc3545';
    } else if (type === 'success') {
        toast.style.background = '#28a745';
    } else if (type === 'warning') {
        toast.style.background = '#ffc107';
        toast.style.color = '#333';
    } else {
        toast.style.background = '#333';
        toast.style.color = 'white';
    }

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ========================================
// PLAY NOTIFICATION SOUND
// ========================================

function playNotificationSound() {
    // Create a simple beep sound using Web Audio API
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();

    oscillator.connect(gain);
    gain.connect(audioContext.destination);

    oscillator.frequency.value = 800;
    oscillator.type = 'sine';

    gain.gain.setValueAtTime(0.3, audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// ========================================
// PAGE VISIBILITY HANDLER
// ========================================

document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        console.log('Page is visible');
    }
});