from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from JMTrucoCmd.models.type_card import TypeCard
class CardBase(BaseModel):
    number: int
    type_cart : Optional[TypeCard] = Field(None)
    #model config
    model_config = ConfigDict(arbitrary_types_allowed=True)

class CardInit(CardBase):
    pass
    


