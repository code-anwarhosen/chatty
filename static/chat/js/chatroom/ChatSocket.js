// chat_room_uid located in chatroom/base.html
const roomUid = JSON.parse(document.getElementById('chat_room_uid').textContent);

// ----------------- Initializing WebSocket ------------------
let protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const ChatSocket = new WebSocket(
    `${protocol}//${window.location.host}/ws/chat/${roomUid}/`
    // ws://127.0.0.1:8000/ws/chat/sdjghj-jsdj-/
);

// ------------------- WebSocket events -------------------
// Show message when WebSocket connection is stabilished
ChatSocket.onopen = function(e) {
    console.log('WebSocket Connection Stabilished!');
};

// populate chat box when received a message
ChatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    const msgObject = {
        type: data.msgType,
        author: data.author,
        content: data.content,
        avatar: data.avatar,
        timestamp: currentTime(),
    };

    insertChatMessage(msgObject);
};

// Show an error message when an error occour
ChatSocket.onerror = function(e) {
    console.error('WebSocket Error!');
};

// Show message when WebSocket connection is closed
ChatSocket.onclose = function(e) {
    console.error('WebSocket Connection Closed');
};


// ------------------- Sending messages -------------------
const inputField = document.getElementById('chat-msg-input');
const sendButton = document.getElementById('chat-msg-send-btn');

// Send message when button is clicked
sendButton.addEventListener('click', function() {
    const message = inputField.value;

    if (String(message).trim().length !== 0){
        ChatSocket.send(JSON.stringify({
            'msgType': 'text',
            'content': message,
        }));
    }
    inputField.value = '';
    inputField.focus();
});

// click send button when enter key is pressed
inputField.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});


// Utility function to return current time like 12:15 PM
function currentTime() {
    const datetime = new Date().toISOString();
    const date = new Date(datetime);
    const hours = date.getHours() % 12 || 12;
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const ampm = date.getHours() >= 12 ? 'PM' : 'AM';
    return `${hours}:${minutes} ${ampm}`;
}