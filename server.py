import argparse
import socket
import threading

from src.game import Game
import src.ui as UI


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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        # AF_INET: Internet address family for IPv4.
        # SOCK_STREAM: Socket type for TCP.
        tcp_socket.bind((HOST, PORT))
        tcp_socket.listen()

        print("Waiting for new connections...")
        while(True):
            print(f"Active sub-threads: {threading.active_count() - 1}")

            # Block and wait for a new connection.
            connection, client_address = tcp_socket.accept()

            # Create a new thread for each connection.
            new_client = threading.Thread(
                group=None, target=client_thread, name=None,
                args=(connection, client_address), kwargs={}, daemon=None
            )
            new_client.start()


def client_thread(connection, client_address):
    with connection:
        # Sends Header asking for user name.
        connection.send(UI.header().encode())

        # Receives user name.
        player_name = connection.recv(1024).decode()

        # Starts the game.
        game = Game(player_name)

        # Starts Round.
        while(True):
            game.start_round()
            player_turn = True
            # Main loop.
            while(True):
                # Sends Scoreboard.
                connection.send(str(game).encode())
                connection.recv(1024)  # Gets an "[OK]"
                if player_turn:
                    # Asks if the player wants more cards.
                    connection.send("[Player's turn]".encode())
                    if connection.recv(1024).decode() == "True":
                        if game.give_card(0):
                            continue
                    player_turn = False

                else:
                    if game.dealer_needs_buy():
                        connection.send("[Dealer's turn]".encode())
                        connection.recv(1024)  # Gets an "[OK]"
                        game.give_card(1)

                    else:
                        connection.send("[End of round]".encode())
                        connection.recv(1024)  # Gets an "[OK]"
                        if game.dealer_won():
                            connection.send(
                                "Sorry, you lost this time...".encode())
                        else:
                            connection.send("Nice! You won!".encode())
                        break

            # Asks if the player wants to play another round.
            if connection.recv(1024).decode() == "False":
                break


if __name__ == "__main__":
    main()
