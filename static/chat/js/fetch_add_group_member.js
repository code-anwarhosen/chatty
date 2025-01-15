// Get modal element
const addMembersModal = document.getElementById('add-members-modal');
function closeAddMembersModal() {
    addMembersModal.classList.add('hidden');
    addMembersModal.classList.remove('flex');
    location.reload(); //reload the page
}

const addMemberBtn = document.getElementById("add-member-btn");
const memberListContainer = document.getElementById("add-member-list");
const memberSearchInput = document.getElementById("member-search-input");
let allUsers = []; // To store fetched users

// chat_room_uid located in chatroom/ group add member modal
const chatGroupUid = JSON.parse(document.getElementById('chat_group_uid').textContent);

// Fetch users when the modal is opened
addMemberBtn.addEventListener("click", async () => {
    try {
        const res = await fetch(`/group/add-member-user-list/${chatGroupUid}/`);
        if (!res.ok) {
            throw new Error("Failed to fetch users");
        }
        let data = await res.json(); // Store users in the variable
        allUsers = data.users;
        populateAddUserList(allUsers); // Populate initial list
    } catch (error) {
        console.error("Error fetching users:", error);
        memberListContainer.innerHTML = `<p class="text-red-500 text-center">Failed to load users.</p>`;
    }

    // Open add member modal
    addMembersModal.classList.remove('hidden');
    addMembersModal.classList.add('flex');
});

// Function to populate user list
function populateAddUserList(users) {
    memberListContainer.innerHTML = ""; // Clear existing user list

    if (users.length === 0) {
        memberListContainer.innerHTML = `<p class="text-gray-400 text-center">No users found.</p>`;
        return;
    }

    users.forEach(user => {
        const userItem = document.createElement("div");
        userItem.className = "flex items-center justify-between py-2 border-b border-slate-600";

        userItem.innerHTML = `
            <div class="flex items-center space-x-3">
                <img src="${user.avatar}" alt="Avatar" class="w-10 h-10 rounded-full">
                <p class="text-gray-300">${user.full_name}</p>
            </div>
            <button onclick="addUserToGroup('${user.username}', this)" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-teal-900">Add</button>
        `;

        memberListContainer.appendChild(userItem);
    });
}

// Function to filter users locally based on search query
memberSearchInput.addEventListener("input", function () {
    const query = this.value.trim().toLowerCase();
    const filteredUsers = allUsers.filter(user =>
        user.full_name.toLowerCase().includes(query)
    );
    populateAddUserList(filteredUsers); // Update the user list
});


// Function to handle adding a user to the group
function addUserToGroup(username, buttonElement) {
    // Data to be sent in the request
    const data = {
        username: username,
        chatgroup_uid: chatGroupUid
    };

    // Send POST request to the server
    fetch('/user/group/add-member/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // Include CSRF token for Django
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            console.log(`${username} successfully added to the group`);
            // Indicate success by updating the button
            buttonElement.innerText = "Added";
            buttonElement.disabled = true;
            buttonElement.classList.remove("bg-blue-500", "hover:bg-teal-900");
            buttonElement.classList.add("bg-green-500", "cursor-not-allowed");
        } else {
            console.log(`Failed to add ${username}: ${result.error}`);
        }
    })
    .catch(error => {
        console.error('Error adding user:', error);
        alert('An error occurred. Please try again.');
    });
}

// Function to get CSRF token from cookies
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return '';
}
