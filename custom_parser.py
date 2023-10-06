import json
import logging
import datetime
import openai
from typing import List
from vocode.streaming.models.transcript import EventLog

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomParsedAppointmentMessage:
    def __init__(self, phoneNumber: int, name: str, appointmentDoctor: str, appointmentTime: datetime):
        self.phoneNumber = phoneNumber
        self.name = name
        self.appointmentDoctor = appointmentDoctor
        self.appointmentTime = appointmentTime


class CustomParser:
    def __init__(self, messages: List[EventLog]):
        self.messages: List[EventLog] = messages

    def parseMessages(self):
        intake_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {'role': 'system', 'content': 'You are assistant that takes in medical data from patients and formats it into JSON'},
                {'role': 'user', 'content': f"Please format the following conversation {self.messages} into a json with these properties name: str, DOB: date, reasonForVisit: str, phoneNumber: int, referringDoctor: str or null if no referring doctor, insuranceProvider: str, insuranceId: str. Please make sure the message returned is a JSON string"}
            ],
            temperature=0,
        )
        appointment_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {'role': 'system', 'content': 'You are assistant that schedules the appointment for the patient'},
                {'role': 'user', 'content': f"Please format the following conversation {self.messages} into a json with these properties phoneNumber: int, name: date, appointmentDoctor: str, appointmentTime: DateTime. Please make sure the message returned is a JSON string"}
            ],
            temperature=0,)
        converted_json_intake = json.loads(
            intake_response.choices[0].message.content)
        converted_json_appointment = json.loads(
            appointment_response.choices[0].message.content)
        # parsedAppointmentMessage = CustomParsedAppointmentMessage(
        #     **converted_json_intake)

        print(converted_json_intake,
              converted_json_appointment)
