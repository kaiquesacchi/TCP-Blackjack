import argparse
import os
import socket


def main():
    # Argument parsing.
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="Host's IPv4",
                        type=str, required=False)
    parser.add_argument("-p", "--port", help="Port", type=int, required=False)
    args = vars(parser.parse_args())

    HOST = args["ip"] if args["ip"] is not None else "localhost"
    PORT = args["port"] if args["port"] is not None else 3000

    # Socket creation.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        # AF_INET: Internet address family for IPv4.
        # SOCK_STREAM: Socket type for TCP.
        connection.connect((HOST, PORT))
        start_game(connection)


def start_game(connection):
    # Shows Header and gets user name.
    name = input(connection.recv(1024).decode())
    if len(name) == 0:
        name = "You"

    # Sends user name to server.
    connection.send(name.encode())

    while(True):
        # Shows Scoreboard and hands.
        os.system('cls' if os.name == 'nt' else 'clear')
        print(connection.recv(1024).decode())
        connection.send("[OK]".encode())

        game_status = connection.recv(1024).decode()

        # Player's turn
        if game_status.startswith("[Player's turn]"):
            while(True):
                buy_card = input("Do you want more cards? [Y/n]: ")
                if buy_card in ["", "y", "Y"]:
                    buy_card = True
                elif buy_card in ["n", "N"]:
                    buy_card = False
                if type(buy_card) == bool:
                    break
            connection.send(str(buy_card).encode())

        # Dealer's turn.
        elif game_status.startswith("[Dealer's turn]"):
            input("Press [Enter] to continue.")
            connection.send("[OK]".encode())

        # End of round.
        else:  # "[End of round]"
            # Shows result.
            connection.send("[OK]".encode())
            print(connection.recv(1024).decode())
            while(True):
                keep_playing = input("Do you want to keep playing? [Y/n]: ")
                if keep_playing in ["", "y", "Y"]:
                    keep_playing = True
                elif keep_playing in ["n", "N"]:
                    keep_playing = False
                if type(keep_playing) == bool:
                    break
            connection.send(str(keep_playing).encode())
            if not keep_playing:
                exit(0)


if __name__ == "__main__":
    main()
