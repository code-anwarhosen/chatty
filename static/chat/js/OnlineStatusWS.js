if (!window.OnlineStatusSocket || window.OnlineStatusSocket.readyState === WebSocket.CLOSED) {
    // ----------------- Initializing WebSocket ------------------
    let protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const OnlineStatusSocket = new WebSocket(
        `${protocol}//${window.location.host}/ws/users/online-status/`
        // ws://127.0.0.1:8000/ws/users/online-status/
    );

    // ------------------- WebSocket events -------------------
    // Show message when WebSocket connection is stabilished
    OnlineStatusSocket.onopen = function(e) {
        console.log('You are online !');

        // i will add more here to update frontend
    };

    // populate chat box when received a message
    OnlineStatusSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const userElement = document.querySelector(`#user-${data.username}`);
        
        if (data.is_online && userElement) {
            userElement.textContent = "Online";
        } else if (userElement) {
            userElement.textContent = "active few seconds ago"
        }
    };

    // Show an error message when an error occour
    OnlineStatusSocket.onerror = function(e) {
        console.error('Online-Status WebSocket Error!');
    };

    // Show message when WebSocket connection is closed
    OnlineStatusSocket.onclose = function(e) {
        console.error('You are offline');
    };
}