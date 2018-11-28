import random
import sys
import socket
import threading
import time


def main():
    # Definição do IP e porta de conexão ______________________________________
    server = "localhost"
    if len(sys.argv) == 1:
        port = 3002

    elif len(sys.argv) == 2:
        port = int(sys.argv[1])

    else:
        print("Uso do programa: python3 servidor.py <porta>")
        exit(1)

    # Criação do socket _______________________________________________________
    print("Iniciando servidor em {}:{}".format(server, port))
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind((server, port))

    # Começa a escutar novas conexões.
    tcp.listen(1)

    while(True):
        print("Aguardando conexão")
        print("Threads ativas: " + str(threading.active_count()))

        # Cria nova thread quando recebe uma nova conexão
        connection, client_address = tcp.accept()
        new_client = threading.Thread(
            group=None, target=client_thread, name=None,
            args=(connection, client_address), kwargs={}, daemon=None
        )
        new_client.start()


full_deck = [(1, '🃁'), (1, '🂡'), (1, '🂱'), (1, '🃑'),
             (2, '🃂'), (2, '🂢'), (2, '🂲'), (2, '🃒'),
             (3, '🃃'), (3, '🂣'), (3, '🂳'), (3, '🃓'),
             (4, '🃄'), (4, '🂤'), (4, '🂴'), (4, '🃔'),
             (5, '🃅'), (5, '🂥'), (5, '🂵'), (5, '🃕'),
             (6, '🃆'), (6, '🂦'), (6, '🂶'), (6, '🃖'),
             (7, '🃇'), (7, '🂧'), (7, '🂷'), (7, '🃗'),
             (8, '🃈'), (8, '🂨'), (8, '🂸'), (8, '🃘'),
             (9, '🃉'), (9, '🂩'), (9, '🂹'), (9, '🃙'),
             (10, '🃊'), (10, '🂪'), (10, '🂺'), (10, '🃚'),
             (10, '🃋'), (10, '🂫'), (10, '🂻'), (10, '🃛'),
             (10, '🃍'), (10, '🂭'), (10, '🂽'), (10, '🃝'),
             (10, '🃎'), (10, '🂮'), (10, '🂾'), (10, '🃞')]


class Game:

    def __init__(self, name):
        self.players = [Player(name), Player('Computer')]

    def show_ui(self):
        # os.system('cls' if os.name == 'nt' else 'clear')
        ui = ''
        for player in self.players:
            ui += (player.name + ": " + str(player.wins) + '\n')
        ui += '\n'
        for player in self.players:
            ui += (player.show_hand() + '\n')
        return ui

    def start_round(self):
        self.deck = full_deck[:]
        for player in self.players:
            player.clear_hand()

    def give_card(self, player_id):
        self.players[player_id].add_card(
            self.deck.pop(random.randint(0, len(self.deck) - 1))
        )

    def need_buy(self):
        return (self.players[0].hand_value() is not 21 and
                not self.players[0].lost() and
                not self.players[1].lost() and
                self.players[0].hand_value() >= self.players[1].hand_value()
                )


class Player:

    def __init__(self, name):
        self.name = name
        self.wins = 0

    def clear_hand(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def hand_value(self):
        value = 0
        has_ace = False
        for card in self.hand:
            value += card[0]
            if card[0] is 1: has_ace = True
        if value < 12 and has_ace: value += 10
        return value

    def show_hand(self):
        ui = ''
        ui += ("Player    : " + self.name + "\n")
        ui += ("Hand Value: " + str(self.hand_value()) + "\n")
        ui += ("Cards     : ")
        for card in self.hand:
            ui += (card[1] + " ")
        ui += "\n"
        return ui

    def lost(self):
        return self.hand_value() > 21


def client_thread(connection, client_address):
    connection.send("Bem Vindo ao BlackJack! Qual o seu nome?".encode())
    name = connection.recv(1024).decode('utf-8')
    game = Game(name)

    while(True):
        game.start_round()
        connection.send(game.show_ui().encode())  # UI
        print(connection.recv(1024).decode())  # "Mesa Recebida"
        connection.send("Posso te entregar uma carta? [S/n]".encode())

        while(connection.recv(1024).decode('utf-8') is not "n"):
            print("Entregando carta")
            game.give_card(0)
            connection.send(game.show_ui().encode())
            print(connection.recv(1024).decode())  # "Mesa Recebida"
            if game.players[0].lost(): break
            connection.send("Posso te entregar uma carta? [S/n]".encode())

        connection.send("[Vez do computador]".encode())
        connection.recv(1024)  # Espera pelo OK

        while(game.need_buy()):
            time.sleep(1)
            game.give_card(1)
            connection.send(game.show_ui().encode())
            connection.recv(1024)  # Mesa Recebida
        if game.players[1].lost() or game.players[0].hand_value is 21:
            game.players[0].wins += 1
            message = "Você Ganhou!"
        else:
            game.players[1].wins += 1
            message = "Você Perdeu..."
        connection.send("{} Quer jogar de novo? [S/n]".format(message).encode())
        if connection.recv(1024).decode('utf-8') is "n": break
    connection.close()


main()
