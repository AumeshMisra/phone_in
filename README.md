# Overview

A phone bot that does medical intake and schedules an appointment

# Requirements

1. brew install poetry
2. brew install ffpeg

# How to run

1. Clone the repo
2. run poetry install
3. In one terminal, run ngrok http 3000
4. In another terminal run, poetry run uvicorn main:app --port 3000
