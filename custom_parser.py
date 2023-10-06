import json
import logging
import datetime
import openai
from typing import List
from pydantic import BaseModel
from vocode.streaming.models.transcript import EventLog

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomParsedIntakeDetails(BaseModel):
    name: str
    dob: datetime
    reasonForVisit: str
    phoneNumber: int
    insuranceProvider: str
    insuranceId: int
    referringDoctor: str


class CustomParsedAppointmentMessage(BaseModel):
    phoneNumber: int
    name: str
    appointmentDoctor: str
    appointmentTime: datetime


class CustomParser:
    def __init__(self, messages: List[EventLog]):
        self.messages: List[EventLog] = messages

    async def parseMessages(self):
        intake_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {
                    "role": "system",
                    "content": "You are assistant that takes in medical data from patients and formats it into JSON",
                },
                {
                    "role": "user",
                    "content": f"Please format the following conversation {self.messages} into a json with these properties name: str, DOB: date, reasonForVisit: str, phoneNumber: int, referringDoctor: str or null if no referring doctor, insuranceProvider: str, insuranceId: str. Please make sure the message returned is a JSON string",
                },
            ],
            temperature=0,
        )
        appointment_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {
                    "role": "system",
                    "content": "You are assistant that schedules the appointment for the patient",
                },
                {
                    "role": "user",
                    "content": f"Please format the following conversation {self.messages} into a json with these properties phoneNumber: int, name: date, appointmentDoctor: str, appointmentTime: DateTime. Please make sure the message returned is a JSON string",
                },
            ],
            temperature=0,
        )
        converted_json_intake: CustomParsedIntakeDetails = CustomParsedIntakeDetails(
            json.loads(intake_response.choices[0].message.content)
        )
        converted_json_appointment: CustomParsedAppointmentMessage = (
            CustomParsedAppointmentMessage(
                json.loads(appointment_response.choices[0].message.content)
            )
        )
        return {
            "json_intake": converted_json_intake,
            "json_appointment": converted_json_appointment,
        }
