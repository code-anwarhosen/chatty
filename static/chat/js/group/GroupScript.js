// When user click on Leave Group Button
function leaveGroup(groupUid) {
    const confirmation = confirm(`You're about to leave this group.`);
    
    if (confirmation) {
        window.location.href = `/user/group/leave-group/${groupUid}/`;
    }
}

// When user click on Delete Group Button
function deleteGroup(groupUid) {
    const confirmation = confirm(`You're about to delete this group.`);
    
    if (confirmation) {
        window.location.href = `/user/group/delete-room/${groupUid}/`;
    }
}