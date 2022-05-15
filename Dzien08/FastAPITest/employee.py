
# Klasa opisująca rekord pracownika
from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Optional
from datetime import datetime

class Employee(BaseModel):
    id : Optional[int] = -1
    fname : str = Field(None, min_length=2, max_length=100)
    lname : str = Field(None, min_length=2, max_length=100)
    pesel : str = ""
    manager : bool = False
    acl : List[int] = []
    create_ts : Optional[datetime] = datetime.now()

    @validator("pesel")
    def pesel_validation(cls, v:str):
        if len(v)==11 and v.isdigit():
            return v
        raise ValueError("Podaj poprawny PESEL")

