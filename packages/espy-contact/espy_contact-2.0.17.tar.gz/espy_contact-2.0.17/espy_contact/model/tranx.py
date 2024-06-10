"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
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
