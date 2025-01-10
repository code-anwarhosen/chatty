
// -------- START: handle search modal toggle (open, close the search modal) --------------
const searchBar = document.getElementById('search-bar'); // this is inside home page
const searchInput = document.getElementById('modal-search-input'); // this is inside modal

const closeModal = document.getElementById('close-modal-btn');
const searchModal = document.getElementById('search-modal');

searchBar.addEventListener('click', () => {
    searchModal.classList.remove('hidden');
    searchModal.classList.add('flex', 'opacity-100');

    searchInput.focus();
    searchInput.value = '';
});

closeModal.addEventListener('click', () => {
    searchModal.classList.add('hidden');
    searchModal.classList.remove('flex', 'opacity-100');
});
// -------- END: handle search modal toggle (open, close the search modal) --------------


// -------------------------------------------------------------------------------------
// --------- START: fetch data, populate modal, filter as user typing -------------------
const userListContainer = document.getElementById('modal-user-list');

// Variable to hold the fetched user list
let allUsers = [];

// Function to fetch the user list from Django when the input field is clicked
searchBar.addEventListener('focus', async () => {
    // Check if the user list is already fetched to avoid repeated requests
    if (allUsers.length === 0) {
        try {
            const response = await fetch('/user-list/'); // call user-list view
            const data = await response.json();
            allUsers = data.users;  // Store the fetched users in the global variable
            populateUserList(allUsers);  // Call to populate the modal with all users

            console.log('users: ', allUsers)
        } catch (error) {
            console.error('Error fetching user list:', error);
        }
    }
});

// Function to filter and display users based on the search input
searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    console.log(query)
    const filteredUsers = allUsers.filter(user => 
        user.username.toLowerCase().includes(query)
    );
    populateUserList(filteredUsers);
});

// Function to populate the modal with users
function populateUserList(users) {
    userListContainer.innerHTML = '';  // Clear current list
    users.forEach(user => {
        const userItem = document.createElement('div');
        userItem.classList.add('user-item');

        userItem.innerHTML = `
            <div class="flex items-center space-x-4 bg-slate-700 p-4 rounded-lg">
                <img src="${user.avatar}" alt="User Avatar" class="w-10 h-10 rounded-full border-2 border-teal-400">
                <a href="/profile/${user.username}/">
                    <p class="text-lg text-gray-300">${user.username}</p>
                </a>
            </div>
        `;
        userListContainer.appendChild(userItem);
    });
}
// --------- END: fetch data, populate modal, filter as user typing -------------------