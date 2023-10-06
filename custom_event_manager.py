import logging
import typing
from fastapi import FastAPI
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.utils import events_manager
from phone_messenger import PhoneMessenger
from custom_parser import CustomParser, CustomParsedAppointmentMessage
from repos.intake import IntakeORM

app = FastAPI(docs_url=None)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# An event manager that process a message, parses a message,
# and sends appointment details to a phone number
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

            # Persist in DB
            intakeORM = IntakeORM()
            await intakeORM.insertIntakeDetails(result['json_intake'])

            # send SMS
            appointmentMessage: CustomParsedAppointmentMessage = result['json_appointment']
            phone_messenger = PhoneMessenger()
            await phone_messenger.sendMessageToNumber(appointmentMessage)
