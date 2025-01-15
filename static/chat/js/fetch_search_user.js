// -------- START: handle search modal toggle (open, close the search modal) --------------
const searchBar = document.getElementById('search-bar'); // this is inside home page
const searchInput = document.getElementById('modal-search-input'); // this is inside modal

const closeModal = document.getElementById('close-modal-btn');
const searchModal = document.getElementById('search-modal');

// Variable to hold the fetched user list
let UserList = [];

// Function to fetch the user list from Django when the input field is clicked
searchBar.addEventListener('click', async () => {
    // Check if the user list is already fetched to avoid repeated requests
    if (UserList.length === 0) {
        try {
            const response = await fetch('/user-list/'); // call user-list view
            const data = await response.json();
            UserList = data.users;  // Store the fetched users in the global variable
            populateUserList(UserList);  // Call to populate the modal with all users
        } catch (error) {
            console.error('Error fetching user list:', error);
        }
    }

    // make open the search modal
    searchModal.classList.remove('hidden');
    searchModal.classList.add('flex');

    // focus and reset value for good ux
    searchInput.focus();
    searchInput.value = '';
});

closeModal.addEventListener('click', () => {
    searchModal.classList.add('hidden');
    searchModal.classList.remove('flex');
});
// -------- END: handle search modal toggle (open, close the search modal) --------------


// --------- START: fetch data, populate modal, filter as user typing -------------------
const userListContainer = document.getElementById('modal-user-list');

// Function to filter and display users based on the search input
searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    const filteredUsers = UserList.filter(user => 
        user.full_name.toLowerCase().includes(query)
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
            <div class="flex items-center space-x-4 bg-slate-700 px-4 py-2 rounded-lg">
                <a href="/auth/user/profile/${user.username}/" class="flex items-center space-x-4">
                    <img src="${user.avatar}" alt="User Avatar" class="w-10 h-10 rounded-full">
                    <p class="text-lg text-gray-300">${user.full_name}</p>
                </a>
            </div>
        `;
        userListContainer.appendChild(userItem);
    });
}
// --------- END: fetch data, populate modal, filter as user typing -------------------