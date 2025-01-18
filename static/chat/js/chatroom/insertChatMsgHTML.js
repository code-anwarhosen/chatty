// This functions is being called from chat_socket when ChatSocket receive a message
function insertChatMessage(message) {
    // Get the chat-box element
    const chatBox = document.getElementById('chat-box');

    // current_user_name located in chatroom/base.html
    let current_user = JSON.parse(document.getElementById('current_user_name').textContent);
    const isCurrentUser = message.author === current_user;

    // generate message based on type
    let messageContentHTML = '';

    if (message.type === 'text') {
        messageContentHTML = `<p class="mt-1">${message.content}</p>`;

    } else if (message.type === 'image') {
        messageContentHTML = `
            <img src="${message.content}" alt="Image" 
                class="mt-1 rounded-lg cursor-pointer" 
                onclick="viewMedia('${message.content}')"/>`;

    } else if (message.type === 'video') {
        messageContentHTML = `
        <video src="${message.content}" controls 
            class="mt-1 rounded-lg cursor-pointer"
            onclick="viewMedia('${message.content}')">
        </video>`;

    } else if (message.type === 'file') {
        const filePath = message.content;
        const baseName = filePath.split('/').pop();
        
        messageContentHTML = `
            <a href="${message.content}" download class="block bg-gray-800 text-white p-2 rounded-lg mt-1 underline">
                <img class="max-h-[30px] place-self-center" src="/static/chat/icons/download.png" alt="download">
                ${baseName}</a>`;
    }
    
    // Generate the HTML structure
    const textMessageHTML = `
        <div class="flex items-start space-x-1 ${isCurrentUser ? 'justify-end' : ''}">
            ${!isCurrentUser ? `<img src="${message.avatar}" alt="User" class="w-8 h-8 rounded-full" />` : ''}
            
            <div class="relative bg-slate-700 p-3 rounded-lg max-w-[60vw]">
                <div class="flex items-center justify-between">
                    <p class="text-sm font-medium">${message.author}</p>
                    <span class="text-xs text-gray-400">${message.timestamp}</span>
                </div>

                ${messageContentHTML}

                <!-- Hover Menu -->
                <div class="message-menu hidden absolute top-0 right-0 mt-1 mr-1 bg-gray-800 text-sm text-white rounded shadow-md">
                    <button class="p-1">Reply</button>
                    <button class="p-1">Edit</button>
                    <button class="p-1">Delete</button>
                </div>
            </div>
        </div>
    `;
    // Append the message HTML to the chat box
    chatBox.insertAdjacentHTML('beforeend', textMessageHTML);


    // this function is in ChatScript.js file
    function scroll(time=0) {
        setTimeout(function () {
            scrollToBottom();
        }, time);
    }
    if (message.type === 'text') {
        scroll(100);
    } else {
        scroll(500);
    }
}
