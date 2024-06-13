from JMTrucoCmd.schemas.type_card import TypeCardInit, TypeCardGet

class TypeCard():
    def __init__(self,type_card_init:TypeCardInit) -> None:
        self.name:str = type_card_init.name.capitalize()
        self.abbrevation:str = type_card_init.name[0:3].upper()
        self.description:str = type_card_init.description
        self.emoji:str = type_card_init.emoji

    def __str__(self) -> str:
        return f'{self.name}'
    
    def get(self,completo=True) -> str:
        if completo:
            return f'{self.name}'
        return f'{self.abbrevation}'
    
    def json(self) -> TypeCardGet:
        return TypeCardGet(
            name=self.name,
            description=self.description,
            abbrevation=self.abbrevation
        )