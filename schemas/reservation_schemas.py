import datetime
from pydantic import BaseModel


class ReservationBase(BaseModel):
    guest_id: int
    start_date: datetime.date
    end_date: datetime.date
    total_price: float


class ReservationAdditionalInfo(ReservationBase):
    id: int

    class Config:
        orm_mode = True


class ReservationCreate(ReservationBase):
    class Config:
        orm_mode = True
