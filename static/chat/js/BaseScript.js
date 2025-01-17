// ---------- START: Hamburger Menu Toggle (Main Menu) ------------------------
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
// ------------- END: Hamburger Menu Toggle (Main Menu) -------------------------


// ------------- START: Profile Dropdown Toggle (User Profile Picture Menu) --------------
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
// --------------------- END: Profile Dropdown Toggle (User Profile Picture Menu) --------------------