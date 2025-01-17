// ------------------- START: Toggle Three-dot Menu (User List Page) ----------------------------
document.querySelectorAll('.three-dot-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
        e.stopPropagation();

        const userItem = btn.closest('.relative'); // Find the closest user item
        const menu = userItem.querySelector('.user-menu'); // Select the menu within the user item

        // Check if the menu is already visible
        const isMenuVisible = menu.classList.contains('show');

        // Close all open menus first
        document.querySelectorAll('.user-menu').forEach((m) => {
            m.classList.remove('show');
        });

        // If the menu was not visible, show it
        if (!isMenuVisible) {
            menu.classList.add('show');
        }
    });
});

// Close menus when clicking outside
window.addEventListener('click', () => {
    document.querySelectorAll('.user-menu').forEach((menu) => {
        menu.classList.remove('show');
    });
});
// ------------------- END: Toggle Three-dot Menu (User List Page) ----------------------------