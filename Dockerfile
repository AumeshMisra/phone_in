FROM python:3.9-bullseye

# get portaudio and ffmpeg
RUN apt-get update \
        && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libasound-dev libsndfile1-dev -y
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

WORKDIR /code
COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock
RUN pip install --no-cache-dir --upgrade poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi
# Potentially need to add line for poetry install evelenlabs==0.2.24
COPY main.py /code/main.py
COPY custom_agent_factory.py /code/custom_agent_factory.py
COPY custom_parser.py /code/custom_parser.py
COPY custom_event_manager.py /code/custom_event_manager.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]