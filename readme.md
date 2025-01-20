# Poke: A Real-Time Chat Application with Django Channels

This is a real-time chat application built using Django, Django Channels, WebSockets, and other modern web technologies. The app supports one-on-one private messaging, group chats, real-time online/offline status updates, message read receipts, and more. It is designed to be responsive, efficient, and scalable.

---

## Features

### User Features

- **One-on-One Private Chats**: Real-time private messaging between two users.
- **Group Chats**: Create groups, add/remove members, and chat with multiple participants.
- **Online/Offline Status**: Real-time updates for online/offline status and "last seen" timestamps.
- **Message Pagination**: Loads the last 20 messages first and supports loading older messages on scroll.
- **Read Receipts**: Indicates whether messages have been read or are still unread.
- **File Sharing**: Supports sharing text, images, videos, audio, and file attachments.

### Admin Features

- Group admins can:
  - Modify group names.
  - Add or remove group members.
  - Delete the group.

### Design

- Fully responsive design optimized for both desktop and mobile screens.
- Dark theme for enhanced readability and user experience.

---

## Installation and Setup

### Prerequisites

1. Python 3.8 or higher.
2. Virtual environment setup (optional but recommended).
3. PostgreSQL (optional for production).

### Steps to Install and Run

1. **Clone the Repository**

   ```bash
   git clone https://github.com/code-anwarhosen/Poke.git
   cd Poke
   ```
2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up the Database**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```
6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000`.

---

## WebSocket Endpoints

- **Chat WebSocket**: Handles real-time messaging within chat rooms.
  ```
  ws://<host>/ws/chat/<room_uid>/
  ```
- **Online Status WebSocket**: Tracks and broadcasts online/offline status.
  ```
  ws://<host>/ws/users/online-status/
  ```

---

## Project Structure

```
├───chat
│   ├───consumers
│   │   └───__pycache__
│   ├───forms
│   │   └───__pycache__
│   ├───migrations
│   ├───views
│   │   └───__pycache__
│   └───__pycache__
├───core
│   └───__pycache__
├───media
│   └───chat
│       └───avatars
│           ├───groups
│           │   └───default
│           └───users
│               └───default
├───static
│   └───chat
│       ├───css
│       ├───icons
│       └───js
│           ├───chatroom
│           ├───group
│           └───home
├───tailwind
│   └───src
└───templates
    └───chat
        ├───chatroom
        ├───components
        ├───group
        ├───home
        ├───pages
        └───user
```

---

## Models Overview

### `ChatRoom`

- Represents chat rooms (private or group).
- Fields: `uid`, `name`, `is_private`, `members`. `avatar`

### `Message`

- Represents messages in chat rooms.
- Fields: `room`, `author`, `content`, `file`, `timestamp`
- Includes a `type` property for determining the message type (e.g., text, image, video).

### `Profile`

- Extends user information for online status tracking.
- Fields: `user`, `is_online`, `last_seen`, `avatar`

---

## Features in Detail

### Online/Offline Status

- **WebSocket Consumer**: `OnlineStatusConsumer`
- Tracks when users connect or disconnect via WebSocket.
- Updates and broadcasts online/offline status to other users in real-time.

### Real-Time Messaging

- **WebSocket Consumer**: `ChatConsumer`
- Handles message sending, receiving, and broadcasting within chat rooms.
- Stores messages in the database and sends them to WebSocket-connected clients.

### Message Pagination

- Loads the last 20 messages when a chat room is opened.
- Older messages are loaded as the user scrolls up.
- Uses AJAX requests for seamless fetching of additional messages.

---

## How to Use the Application

1. **Log in or Register**: Use the authentication system to log in or create an account.
2. **Chat List**: View your active one-on-one and group chats.
3. **Start a Chat**:
   - For private chats, find a user and start a conversation.
   - For group chats, create a new group and add members.
4. **Send Messages**:
   - Type text, attach files, or send media in real time.
   - View message read receipts and online/offline indicators.
5. **Scroll to Load Older Messages**: View older messages by scrolling up in the chat.

---

## Future Enhancements

1. **Push Notifications**: Notify users of new messages even when they're offline.
2. **End-to-End Encryption**: Secure all communication within the app.
3. **Search Functionality**: Add search capabilities for messages and users.
4. **Video and Audio Calls**: Enable real-time voice and video communication.

---

## Screenshots

- will add later

---

## Contribution

We welcome contributions to improve this project. To contribute:

1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Open a pull request with a detailed description of your changes.

---

## License

This project is open-source and licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to report issues or suggest enhancements. Enjoy building and using this real-time chat app!

---

## Author

**Anwar Hosen**
A passionate learner and developer building real-time applications and exploring modern web technologies.

- GitHub: [@code-anwarhosen](https://github.com/code-anwarhosen)

---
