def header():
    return '''\
========================================
        Welcome to TCP-Blackjack       
========================================

Please, tell us your name: '''


def scoreboard(players):
    message = '''\
========================================
               Scoreboard
----------------------------------------
'''
    for player in players:
        message += f"{player.name}: {player.wins}\n"
    message += '''\
----------------------------------------
'''
    for player in players:
        message += f"{player.show_hand()}\n"
    message += '''\
========================================

'''
    return message


def show_hand(player):
    message = f'''
Player    : {player.name}
Hand Value: {player.hand_value()}
Cards     :'''
    for card in player.hand:
        message += (f" {card[1]}")
    message += "\n"
    return message


def won():
    return '''\
========================================
             Nice! You Won!
========================================
'''


def lost():
    return '''\
========================================
           Oh no... You lost!
========================================
'''
