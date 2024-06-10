from espy_contact.util.db import Base
from espy_contact.util.enums import StatusEnum
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, ForeignKey, Text, Date, Float,Enum
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.orm import relationship


class Tranx(Base):
    __tablename__ = "tranx"

    ref = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stripeId = Column(String)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    payee_id = Column(Integer, ForeignKey("appusers.id"))
    detail = Column(Text)  # Text allows for larger details if needed
    createdOn = Column(DateTime(), server_default=func.now())
    modifiedOn = Column(DateTime(), onupdate=func.now())
    raw_json = Column(Text)  # This can be used to store the raw json response from the payment gateway

    payee = relationship("Appuser", backref="transactions")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bank = Column(String, nullable=False)  # Assuming NigerianBank is a string enum
    account_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    account_officer = Column(String)
    account_admin = Column(String)
    created_on = Column(DateTime, default=datetime)
    modified_on = Column(DateTime, onupdate=datetime)


class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    status = Column(Enum(StatusEnum))

    classroom = relationship("Classroom")
