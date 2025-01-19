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
    
    } else if (message.type === 'audio') {
        messageContentHTML = `
            <audio src="${message.content}" controls 
                class="mt-3 w-[200px] md:w-[300px] lg:w-[400px] cursor-pointer">
                Your browser does not support the audio element.
            </audio>`;

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
            <a href="${message.content}" download class="block bg-gray-800 text-white p-2 rounded-lg mt-1 underline break-words">
                <img class="max-h-[30px] place-self-center" src="/static/chat/icons/download.png" alt="download">
                ${baseName}</a>`;
    }
    
    // Generate the HTML structure
    const textMessageHTML = `
        <div class="flex items-start space-x-1 ${isCurrentUser ? 'justify-end' : ''}">
            ${!isCurrentUser ? `<img src="${message.avatar}" alt="User" class="w-6 h-6 rounded-full" />` : ''}
            
            <div class="relative bg-slate-700 px-2 py-1 rounded-lg max-w-[60vw]">

                ${!isCurrentUser && !message?.is_private_room ? `
                    <div class="flex items-center justify-between">
                        <p class="text-xs font-light text-gray-400">${message?.author || 'Unknown'}</p>
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
