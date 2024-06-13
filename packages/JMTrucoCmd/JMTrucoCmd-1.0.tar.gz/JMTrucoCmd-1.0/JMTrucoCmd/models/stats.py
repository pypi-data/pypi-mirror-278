from JMTrucoCmd.schemas.stats import StatsInit

class Stats():
    def __init__(self,stats_init:StatsInit) -> None:
        self.aggressive:int =  self.max_and_minum_init_stats(stats_init.aggressive)
        self.fisherman:int = self.max_and_minum_init_stats(stats_init.fisherman)
        self.liar:int = self.max_and_minum_init_stats(stats_init.liar)
        self.score_truco:int = stats_init.score_truco
        self.score_envido:int = stats_init.score_envido

    def __str__(self) -> str:
        return f'agresivo: {self.aggressive}, mentiroso: {self.liar}, pescador:{self.fisherman}'#, score_truco:{self.score_truco}, score_envido:{self.score_envido}'

    def max_and_minum_init_stats(self, n):
        if n<=0:
            return 1
        if n>=11:
            return 10
        return n