// chat_room_uid located in chatroom/base.html
const roomUid = JSON.parse(document.getElementById('chat_room_uid').textContent);

// ----------------- Initializing WebSocket ------------------
let protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const ChatSocket = new WebSocket(
    `${protocol}//${window.location.host}/ws/chat/${roomUid}/`
    // ws://127.0.0.1:8000/ws/chat/sdjghj-jsdj-/
);

// ------------------- WebSocket events -------------------
ChatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    const msgObject = {
        type: data.message_type,
        author: data.author,
        content: data.message,
        created_at: new Date().toISOString()
    };
    if (msgObject.type === 'text') {
        addTextMessageToChatBox(msgObject);
    }
};

// Show an error message when WebSocket connection is closed
ChatSocket.onclose = function(e) {
    console.error('WebSocket closed unexpectedly');
};


// ------------------- Sending messages -------------------
const inputField = document.getElementById('chat-msg-input');
const sendButton = document.getElementById('chat-msg-send-btn');

// Send message when button is clicked
sendButton.addEventListener('click', function() {
    const message = inputField.value;
    console.log("Message:", message);

    if (String(message).trim().length !== 0){
        ChatSocket.send(JSON.stringify({
            'message': message
        }));
    }
    inputField.value = '';
});

// click send button when enter key is pressed
inputField.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});
