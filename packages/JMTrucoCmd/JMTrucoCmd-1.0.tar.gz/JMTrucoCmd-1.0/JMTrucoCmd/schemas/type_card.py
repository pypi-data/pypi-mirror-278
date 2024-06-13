from pydantic import BaseModel
from typing import List, Optional

class TypeCardBase(BaseModel):
    name: str
    description: str
    emoji:str
    

class TypeCardInit(TypeCardBase):
    pass

class TypeCardGet(TypeCardBase):
    abbrevation:str

