from pydantic import BaseModel
from typing import List, Optional
from JMTrucoCmd.schemas.card import CardInit

class CardsBase(BaseModel):
    cards: list
    
class CardsInit(CardsBase):
    pass

