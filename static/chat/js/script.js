// START: Hamburger Menu Toggle (Main Menu)
const menuBtn = document.getElementById('menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
let menuOpen = false;

menuBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent click from closing the menu
    menuOpen = !menuOpen;
    toggleMenu();
});

window.addEventListener('click', () => {
    if (menuOpen) {
        menuOpen = false;
        toggleMenu();
    }
});

mobileMenu.addEventListener('click', (e) => e.stopPropagation()); // Prevent clicks inside the menu from closing it

function toggleMenu() {
    if (menuOpen) {
        mobileMenu.classList.remove('hidden');
        setTimeout(() => mobileMenu.classList.remove('opacity-0'), 10);
    } else {
        mobileMenu.classList.add('opacity-0');
        setTimeout(() => mobileMenu.classList.add('hidden'), 300);
    }
}
// END: Hamburger Menu Toggle (Main Menu)
//---------------------------------------------------------------------------------

// START: Profile Dropdown Toggle (User Profile Picture Menu)
const profileBtn = document.getElementById('profile-btn');
const profileDropdown = document.getElementById('profile-dropdown');
let dropdownOpen = false;

profileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdownOpen = !dropdownOpen;
    toggleDropdown();
});

window.addEventListener('click', () => {
    if (dropdownOpen) {
        dropdownOpen = false;
        toggleDropdown();
    }
});

profileDropdown.addEventListener('click', (e) => e.stopPropagation());

function toggleDropdown() {
    if (dropdownOpen) {
        profileDropdown.classList.remove('hidden');
        setTimeout(() => profileDropdown.classList.remove('opacity-0'), 10);
    } else {
        profileDropdown.classList.add('opacity-0');
        setTimeout(() => profileDropdown.classList.add('hidden'), 200);
    }
}
// END: Profile Dropdown Toggle (User Profile Picture Menu)
//---------------------------------------------------------------------------------

// START: Three-dot Menu Toggle for Each User (User List Page, Three Dot Menu On the Right Side of Each User)
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
// END: Three-dot Menu Toggle for Each User (User List Page, Three Dot Menu On the Right Side of Each User)
//---------------------------------------------------------------------------------