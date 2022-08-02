import datetime
from typing import Optional

from pydantic import BaseModel


class Projects(BaseModel):

    id: int
    title: str
    link: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
