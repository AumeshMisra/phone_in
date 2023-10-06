import logging
import typing
from fastapi import FastAPI
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.utils import events_manager
from phone_messenger import PhoneMessenger
from custom_parser import CustomParser, CustomParsedAppointmentMessage

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
            appointmentMessage: CustomParsedAppointmentMessage = result['json_appointment']
            print(appointmentMessage)
            # go thourgh persisting data to DB
            # go through messaging back phone
            # {'json_intake': {'name': 'Aumesh', 'DOB': '1998-10-02', 'reasonForVisit': 'Broken Neck', 'phoneNumber': 4085945927, 'referringDoctor': 'Doctor Shai', 'insuranceProvider': 'Aetna', 'insuranceId': '111'}, 'json_appointment': {'phoneNumber': 4085945927, 'name': 'Aumesh', 'appointmentDoctor': 'Dr. Michael Johnson', 'appointmentTime': 'Friday at 2 PM'}}
            phone_messenger = PhoneMessenger()
            phone_messenger.sendMessageToNumber(appointmentMessage)
