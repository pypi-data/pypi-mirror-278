from random import choice
from time import sleep
#models
from JMTrucoCmd.models.type_card import TypeCard
from JMTrucoCmd.models.card import Card
#schemas
from JMTrucoCmd.schemas.type_card import TypeCardInit, TypeCardGet
from JMTrucoCmd.schemas.card import CardInit

def get_deck():
    deck = []
    type_carts:list = [
        TypeCard(
            TypeCardInit(
                name='Espada',
                description='Tipo de carta: espada',
                emoji= '🔪'
            )
        ),
        TypeCard(
            TypeCardInit(
                name='basto',
                description='Tipo de carta: basto',
                emoji = '🌳'
            )
        ),
        TypeCard(
            TypeCardInit(
                name='oro',
                description='Tipo de carta: oro',
                emoji = '🥇'
            )
        ),
        TypeCard(
            TypeCardInit(
                name='copa',
                description='Tipo de carta: copa',
                emoji = '🥂'
            )
        ),
    ]
    numbers = {
        1:1,
        2:2,
        3:3,
        4:4,
        5:5,
        6:6,
        7:7,
        8:10,
        9:11,
        0:12
    }
    cont = 0
    for i in range(1,41):
        n = i%10
        cart =Card(
            CardInit(number=numbers[n], type_cart=type_carts[cont])
        )
        deck.append(cart)
        if n==0:
            cont+=1
    return deck

def get_cards():
    deck = get_deck()
    carts = []
    for i in range(6):
        cart:Card = choice(deck)
        carts.append(cart)
        deck.remove(cart)
    return carts

def calculate_envido(cards:list):
    envido_points = 0
    no_envido = cards[-1].get_envido()
    for i in range(len(cards)-1):
        if cards[i].get_envido() > no_envido:
            no_envido = cards[i].get_envido()
        for j in range(i+1,len(cards)):
            if cards[i].type_card == cards[j].type_card:
                points = 20 + cards[i].get_envido() + cards[j].get_envido()
                if not envido_points:
                    envido_points = points
                elif envido_points < points:
                    envido_points = points
    return max(envido_points,no_envido)

def calculate_truco(cards:list):
    truco_points = 0
    for card in cards:
        truco_points+=card.value
    return truco_points

def calculate_win(cards_played:dict):
    response = {
        'pc': 0,
        'player': 0,
        'draw':0
    }
    bot_responses = False
    if (len(cards_played['player']) > len(cards_played['pc'])):
        bot_responses = cards_played['player'][-1]
    
    quantity = min(len(cards_played['pc']),len(cards_played['player']))
    
    for i in range(quantity):
        if cards_played['pc'][i].value < cards_played['player'][i].value:
            response['pc']+=1
        elif cards_played['pc'][i].value > cards_played['player'][i].value:
            response['player']+=1
        else:
            response['draw']+=1
    
    return response, bot_responses
