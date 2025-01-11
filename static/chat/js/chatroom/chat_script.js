// ------- function to open chat media in new tab -------------
function viewMedia(url) {
window.open(url, '_blank');
}

// ----- function to scroll to bottom of the chat ------------
function scrollToBottom() {
const mainContainer = document.querySelector('main');
mainContainer.scrollTop = mainContainer.scrollHeight;
}
scrollToBottom();

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