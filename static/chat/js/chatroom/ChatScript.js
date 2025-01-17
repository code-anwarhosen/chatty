// ------- function to open chat media in new tab -------------
function viewMedia(url) {
window.open(url, '_blank');
}

// chat-box container
const chatContainer = document.getElementById('chat-box');

// function to scroll to bottom of chat-box
function scrollToBottom() {
    const lastMessage = chatContainer.lastElementChild;
    if (lastMessage) {
        lastMessage.scrollIntoView({ behavior: 'smooth' });
    }
}

// ----- START: Scroll to bottom of the chat when the page loads ------------
window.addEventListener('load', () => {
    scrollToBottom();
});
// ----- END: Scroll to bottom of the chat when the page loads ------------

// START: Show scroll button if user scroll up in chat box -------------------------
chatContainer.addEventListener('scroll', () => {
    const scrollDownBtn = document.getElementById('scroll-down-btn');

    const threshold = 50;
    const isAtBottom = chatContainer.scrollHeight - chatContainer.scrollTop <= chatContainer.clientHeight + threshold;

    if (isAtBottom) {
        scrollDownBtn.style.display = 'none';
    } else {
        scrollDownBtn.style.display = 'block';
    }
});
// START: Show scroll button if user scroll up in chat box -------------------------


// ----------- START: Function to toggle message's hover menu (Reply, Edit, Delete) -----------
function toggleMenu(event) {
    const msgContainer = event.target.closest('.relative');
    if (!msgContainer) return; // Ensure it's a valid message container

    const menu = msgContainer.querySelector('.message-menu');
    if (menu) {
        closeAllMenus();
        menu.classList.remove('hidden');
    }
}

// Close all open menus
function closeAllMenus() {
    document.querySelectorAll('.message-menu').forEach(menu => menu.classList.add('hidden'));
}

// Attach mouseenter and mouseleave events using event delegation
const chatBox = document.getElementById('chat-box');
chatBox.addEventListener('mouseenter', toggleMenu, true);
chatBox.addEventListener('mouseleave', closeAllMenus, true);

// Prevent closing menu when interacting with it
chatBox.addEventListener('click', event => {
    if (event.target.closest('.message-menu')) {
        event.stopPropagation();
    }
});
// ----------- END: Function to toggle message's hover menu (Reply, Edit, Delete) -----------