"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel
from espy_contact.util.enums import StatusEnum, NigerianBank
class AccountDto(BaseModel):
    id: Optional[int] = None
    bank: NigerianBank
    account_name: str
    account_number: str
    currency: str
    is_active: bool
    account_officer: str
    account_admin: str
    created: datetime
    modified: datetime


class FeeDto(BaseModel):
    classroom_id: str
    fee_name: str
    amount: float
    due_date: date
    start_date: date
    status: StatusEnum
