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
const menu = event.target.closest('.relative').querySelector('.message-menu');
if (menu.classList.contains('hidden')) {
    closeAllMenus();
    menu.classList.remove('hidden');
} else {
    menu.classList.add('hidden');
}
}

// Close all open menus
function closeAllMenus() {
document.querySelectorAll('.message-menu').forEach(menu => menu.classList.add('hidden'));
}

// Attach mouseenter and mouseleave events to message containers
document.querySelectorAll('.relative').forEach(msg => {
msg.addEventListener('mouseenter', toggleMenu);
msg.addEventListener('mouseleave', closeAllMenus);
});

// Prevent closing menu when interacting with it
document.querySelectorAll('.message-menu').forEach(menu => {
menu.addEventListener('click', event => event.stopPropagation());
});
// ----------- END: Function to toggle message's hover menu (Reply, Edit, Delete) -----------