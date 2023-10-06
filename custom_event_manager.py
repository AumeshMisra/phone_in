import logging
import typing
from fastapi import FastAPI
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.utils import events_manager

from custom_parser import CustomParser

app = FastAPI(docs_url=None)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomEventsManager(events_manager.EventsManager):
    def __init__(self):
        super().__init__(subscriptions=[
            EventType.TRANSCRIPT_COMPLETE])

    async def handle_event(self, event: Event):
        if event.type == EventType.TRANSCRIPT_COMPLETE:
            transcript_complete_event = typing.cast(
                TranscriptCompleteEvent, event)
            # Handle processing the transcript
            custom_parser = CustomParser(
                transcript_complete_event.transcript.event_logs)
            custom_parser.parseMessages()
