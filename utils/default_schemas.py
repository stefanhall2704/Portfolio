import datetime
from typing import Optional

from pydantic import BaseModel


class Projects(BaseModel):

    id: int
    title: str
    link: str
    first_name: str
    last_name: str
    picture: str
    user_id: int

    class Config:
        orm_mode = True


class ApplicationUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str

    class Config:
        orm_mode = True
