import os
import logging
from twilio.rest import Client
from vocode.streaming.models.telephony import TwilioConfig

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PhoneMessenger:
    def __init__(self):
        account_sid = os.environ["TWILIO_ACCOUNT_SID"],
        auth_token = os.environ["TWILIO_AUTH_TOKEN"],
        self.client = Client(account_sid, auth_token)

    async def sendMessageToNumber(self, json_appointment):
        message = self.client.messages.create(
            body=f"Scheduled appointment with {json_appointment.appointmentDoctor} at {json_appointment.appointmentTime}",
            to=f"{json_appointment.phoneNumber}"
        )
        return message
