from models.database_start import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, BigInteger


class Intake(Base):
    __tablename__ = "intake"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    dob = Column(String)
    reasonForVisit = Column(String)
    phoneNumber = Column(BigInteger)
    insuranceProvider = Column(String)
    insuranceId = Column(String)
    referringDoctor = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
