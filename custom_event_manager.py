import logging
import typing
from fastapi import FastAPI
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.utils import events_manager
from phone_messenger import PhoneMessenger
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
            result = await custom_parser.parseMessages()
            print(result)
            # go thourgh persisting data to DB
            # go through messaging back phone
            phone_messenger = PhoneMessenger()
            phone_messenger.sendMessageToNumber(result.json_appointment)
