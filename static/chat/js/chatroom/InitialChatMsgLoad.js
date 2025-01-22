
// This functions is being called from chat_socket when ChatSocket receive a message
function insertPaginateChatMessage(chatBox, message) {

    // current_user_name located in chatroom/main.html
    let current_user = JSON.parse(document.getElementById('current_user_name').textContent);
    const isCurrentUser = current_user === message.author;
    
    // generate message based on type
    let messageContentHTML = '';

    if (message.type === 'text') {
        messageContentHTML = `<p class="mt-1">${message.content}</p>`;

    } else if (message.type === 'image') {
        messageContentHTML = `
            <img src="${message.file_url}" alt="Image" 
                class="mt-1 rounded-lg cursor-pointer" 
                onclick="viewMedia('${message.file_url}')"/>`;
    
    } else if (message.type === 'audio') {
        messageContentHTML = `
            <audio src="${message.file_url}" controls 
                class="mt-3 w-[200px] md:w-[300px] lg:w-[400px] cursor-pointer">
                Your browser does not support the audio element.
            </audio>`;

    } else if (message.type === 'video') {
        messageContentHTML = `
        <video src="${message.file_url}" controls 
            class="mt-1 rounded-lg cursor-pointer"
            onclick="viewMedia('${message.file_url}')">
        </video>`;

    } else if (message.type === 'file') {
        const filePath = message.file_url;
        const baseName = filePath.split('/').pop();
        
        messageContentHTML = `
            <a href="${message.file_url}" download class="block bg-gray-800 text-white p-2 rounded-lg mt-1 underline break-words">
                <img class="max-h-[30px] place-self-center" src="/static/chat/icons/download.png" alt="download">
                ${baseName}</a>`;
    }
    
    // Generate the HTML structure
    const textMessageHTML = `
        <div class="flex items-start space-x-1 ${isCurrentUser ? 'justify-end' : ''}">
            ${!isCurrentUser ? `<img src="${message.avatar_url}" alt="User" class="w-6 h-6 rounded-full" />` : ''}
            
            <div class="relative bg-slate-700 px-2 py-1 rounded-lg max-w-[60vw]">

                ${!isCurrentUser && !message?.is_private_room ? `
                    <div class="flex items-center justify-between">
                        <p class="text-xs font-light text-gray-400">${message?.full_name || 'Unknown'}</p>
                    </div>
                ` : ''}

                ${messageContentHTML}

                <!-- Hover Menu -->
                <div class="message-menu hidden absolute top-0 right-0 mt-1 mr-1 bg-gray-800 text-sm text-white rounded shadow-md z-20">
                    <span class="p-1 text-xs text-gray-400">${message.timestamp}</span>    
                    <!-- <button class="p-1">Delete</button> -->
                </div>
            </div>
        </div>
    `;
    // Append the message HTML to the chat box
    chatBox.insertAdjacentHTML('afterbegin', textMessageHTML);
}


// ------------ Fetch Messages When User Open a Chat -------------------------
const ChatBox = document.getElementById('chat-box');
const ROOM_UID = JSON.parse(document.getElementById('chat_room_uid').textContent);

let offset = 0; // Start at the most recent messages
const limit = 10; // Number of messages to load at a time

let hasMoreMessages = true; // Flag to track if there are more messages to load
let isLoading = false; // Prevent multiple simultaneous requests
const loadMore = document.getElementById('load-more-btn');

// Fetch messages from the backend
async function fetchMessages() {
    if (!hasMoreMessages || isLoading) {
        loadMore.classList.add('hidden');
        return;
    }

    isLoading = true;
    const loadingSpinner = document.getElementById('loading-spinner');
    loadingSpinner.style.display = 'block';

    try {
        const response = await fetch(`/chat/${ROOM_UID}/messages/?offset=${offset}&limit=${limit}`);
        const data = await response.json();

        if (data.success) {
            const messages = data.messages;

            if (messages.length > 0) {
                messages.forEach((message) => {
                    let msgObj = {
                        author: message.author,
                        full_name: message.full_name,

                        avatar_url: message.avatar_url,
                        content: message.content,
                        file_url: message.file_url,

                        type: message.type,
                        timestamp: message.timestamp,
                        is_private_room: message.is_private_room,
                    }
                    insertPaginateChatMessage(ChatBox, msgObj);
                });

                // Update offset
                offset += messages.length;
            } else {
                hasMoreMessages = false; // No more messages to load
            }
        } else {
            console.error('Failed to load messages:', data.error);
        }
    } catch (error) {
        console.error('Error fetching messages:', error);
    } finally {
        isLoading = false;
        loadingSpinner.style.display = 'none';
    }
}

// Initial load of the most recent messages
fetchMessages();
setTimeout(function () {
    const lastMessage = ChatBox.lastElementChild;
    if (lastMessage) {
        lastMessage.scrollIntoView({ behavior: 'smooth' });
    }
}, 1000);

// Listen for scroll event on the chat box
ChatBox.addEventListener('scroll', () => {

    if (ChatBox.scrollTop <= 20 && !isLoading && hasMoreMessages) {
        loadMore.classList.remove('hidden');
    } else {
        loadMore.classList.add('hidden');
    }
});