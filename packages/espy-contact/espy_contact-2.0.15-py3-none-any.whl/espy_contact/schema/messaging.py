from pydantic import BaseModel,EmailStr
from typing import Optional,List
from datetime import datetime

class Message(BaseModel):
    id: int
    sender: str
    recipient: str
    content: str
class MailerDto(BaseModel):
    recipients: List[EmailStr]
    subject: str
    message: str
    create_at: Optional[datetime] = datetime.now()
    is_html: bool