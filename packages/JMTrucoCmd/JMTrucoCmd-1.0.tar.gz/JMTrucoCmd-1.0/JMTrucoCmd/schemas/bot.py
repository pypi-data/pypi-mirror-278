from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from JMTrucoCmd.models.stats import Stats
from JMTrucoCmd.schemas.stats import StatsInit


class BotBase(BaseModel):
    name: str
    stats:Stats

    #model config
    model_config = ConfigDict(arbitrary_types_allowed=True)

class BotInit(StatsInit):
    name: Optional[str] = None
    phrases: Optional[dict] = None


    


