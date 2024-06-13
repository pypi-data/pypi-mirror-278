#models
from JMTrucoCmd.models.bot import Bot
#schemas
from JMTrucoCmd.schemas.bot import BotInit
#data
from JMTrucoCmd.data.bots import bots_data

def get_bots(name=None):
    if name:
        name = name.title()
        return Bot(bots_data[name])
    bots = []
    for i in bots_data:
        bots.append(Bot(bots_data[i]))
    return bots