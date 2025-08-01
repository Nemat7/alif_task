from datetime import datetime
from dataclasses import dataclass

@dataclass
class Booking:
    cabinet_number: int
    start_time: datetime
    end_time: datetime
    user_name: str
    user_email: str
    user_phone: str



