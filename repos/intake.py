from models.models import Intake
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.database_start import engine


class IntakeDetails(BaseModel):
    name: Optional[str]
    dob: Optional[datetime]
    reasonForVisit: Optional[str]
    phoneNumber: Optional[int]
    insuranceProvider: Optional[str]
    insuranceId: Optional[str]
    referringDoctor: Optional[str]


class IntakeORM:
    def __init__(self):
        self.connection = engine.connect()

    async def insertIntakeDetails(self, intake_details: IntakeDetails):
        if (intake_details):
            intake: Intake = Intake(name=intake_details.name,
                                    dob=intake_details.dob,
                                    reasonForVisit=intake_details.reasonForVisit,
                                    phoneNumber=intake_details.phoneNumber,
                                    insuranceProvider=intake_details.insuranceProvider,
                                    insuranceId=intake_details.insuranceId,
                                    referringDoctor=intake_details.referringDoctor)
            session = Session(bind=self.connection)
            session.add(intake)
            session.commit()
            session.close()

    async def fetchAll(self):
        session = Session(bind=self.connection)
        result = session.query(Intake).all()
        session.close()
        return result
