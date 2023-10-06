# Overview

A phone bot that does medical intake and schedules an appointment

# Requirements

1. brew install poetry
2. brew install ffpeg
3. brew install portaudio
4. brew install ngrok

# How to run

1. Clone the repo
2. Get all the appropriate api keys in your .env file
3. run ```poetry install```
4. run ```brew services start redis```
5. In one terminal, run ```ngrok http 3000```
6. Copy the url from ngrok and paste into both twilio and BASE_URL in your .env file
7. In another terminal run, ```poetry run uvicorn main:app --port 3000```
8. Call your twilio number
