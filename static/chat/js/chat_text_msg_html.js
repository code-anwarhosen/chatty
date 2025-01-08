function addTextMessageToChatBox(message) {
    // Get the chat-box element
    const chatBox = document.getElementById('chat-box');

    // Determine if the message was sent by the current user
    // const isCurrentUser = message.author === "{{ request.user.username }}";

    let current_user = JSON.parse(document.getElementById('current_user_name').textContent);
    const isCurrentUser = message.author === current_user;

    // Generate the HTML structure
    const textMessageHTML = `
        <div class="flex items-start space-x-1 ${isCurrentUser ? 'justify-end' : ''} transition-all duration-300 opacity-0">
            ${!isCurrentUser ? '<img src="https://via.placeholder.com/40" alt="User" class="w-8 h-8 rounded-full" />' : ''}
            
            <div class="relative bg-slate-700 p-3 rounded-lg max-w-[60vw]">
                <div class="flex items-center justify-between">
                    <p class="text-sm font-medium">${message.author}</p>
                    <span class="text-xs text-gray-400">${formatTime(message.created_at)}</span>
                </div>
                <p class="mt-1">${message.content}</p>

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

    // Find the last inserted message and trigger the transition
    const lastMessage = chatBox.lastElementChild;
    lastMessage.classList.remove('opacity-0');
    lastMessage.classList.add('opacity-100');

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Utility function to format time (if needed)
function formatTime(datetime) {
    const date = new Date(datetime);
    const hours = date.getHours() % 12 || 12;
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const ampm = date.getHours() >= 12 ? 'PM' : 'AM';
    return `${hours}:${minutes} ${ampm}`;
}
