# Django Chat Application

This is a real-time chat application built using Django, Django Channels, and WebSockets.

## Features

- Real-time chat functionality
- User authentication
- Group chat functionality
- Send text, images, audio, and video

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/code-anwarhosen/chatty.git
   ```
2. Move to project directory

   ```
   cd chatty
   ```
3. Install requirements.txt

   ```
   pip install -r requirements.txt
   ```
4. run with manage.py

   ```
   python manage.py runserver
   ```

   or with daphne

   ```
   daphne core.asgi:application --bind 0.0.0.0 --port 8000
   ```


Docker

```
docker build -t chatty .
```

```
docker compose up -d
```

Just run these and access it in local ip at port 80 (django + postgres + redis + nginx)
