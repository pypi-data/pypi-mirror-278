from JMTrucoCmd.schemas.card import CardInit

class Card():
    def __init__(self,card_init:CardInit, valid_numbers = [1,2,3,4,5,6,7,10,11,12]) -> None:
        
        if card_init.number in valid_numbers:
            self.number:int = card_init.number
        else: 
            self.number:int = valid_numbers[0]
        
        self.type_card = card_init.type_cart
        self.value = self.get_value()

    def __str__(self) -> str:
        return f'{self.number} {self.type_card}'
    
    
    def get(self,completo=True) -> str:
        return f'{self.number} {self.type_card.get(completo=completo)}'
    
    def get_value(self):
        values_normal = {
            3: 5,
            2: 6,
            12: 8,
            11: 9,
            10: 10,
            6: 12,
            5: 13,
            4: 14
        }
        if self.number in values_normal:
            return values_normal[self.number]
        elif self.number == 1:
            values_1 = {
                'Espada':1,
                'Basto':2,
                'Oro':7,
                'Copa':7,
            }
            if self.type_card.name in values_1:
                return values_1[self.type_card.name]
        elif self.number == 7:
            values_7 = {
                'Espada':3,
                'Basto':11,
                'Oro':4,
                'Copa':11,
            }
            if self.type_card.name in values_7:
                return values_7[self.type_card.name]
        return 0

    def get_envido(self):
        if self.number in [10,11,12]:
            return 0
        return self.number