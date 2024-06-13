from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class StatsBase(BaseModel):
    liar: Optional[int] = None
    fisherman: Optional[int] = None
    aggressive: Optional[int] = None
    score_truco: Optional[int] = None
    score_envido: Optional[int] = None

    #model config
    model_config = ConfigDict(arbitrary_types_allowed=True)

class StatsInit(StatsBase):
    pass
    


