import socket
import sys
import os


def main():
    # Definição do IP e porta de conexão
    if len(sys.argv) == 1:
        server = 'localhost'
        port   = 3002

    elif len(sys.argv) == 3:
        server = sys.argv[1]
        port   = int(sys.argv[2])

    else:
        print("Uso do programa: python3 cliente.py <host> <porta>")
        print("Valores padrão: 'localhost:3000'")
        exit(1)

    # Criação do socket
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Conectando a {}:{}".format(server, port))

    # Requisição
    tcp.connect((server, port))
    play(tcp)


def play(tcp):
    # Recebe mensagem de Boas vindas
    print(tcp.recv(1024).decode())

    # Envia o nome do jogador
    tcp.send(input("").encode())

    while(True):
        while(True):
            # Recebe Mesa ou [Vez do computador]
            message = tcp.recv(1024).decode('utf-8')
            if message.startswith("[Vez do computador]"): break

            # Envia "Mesa recebida" e imprime o mapa
            tcp.send("Mesa recebida".encode())
            os.system('cls' if os.name == 'nt' else 'clear')
            print(message)

            # Recebe 'Quer comprar carta' ou [Vez do computador]
            message = tcp.recv(1024).decode('utf-8')
            if message.startswith("[Vez do computador]"): break
            print(message)

            # Envia resposta (Quer ou não comprar carta)
            tcp.send(input("").encode())

        # Envia "[Vez do computador]"
        tcp.send("[Vez do computador]".encode())

        while(True):
            # Recebe Mesa ou 'Você Ganhou/Perdeu'
            message = tcp.recv(1024).decode()
            if message.startswith("Você"): break
            os.system('cls' if os.name == 'nt' else 'clear')
            print(message)

            # Envia um OK
            tcp.send("Mensagem recebida".encode())

        # Envia a resposta
        print(message)
        resposta = input("")
        tcp.send(resposta.encode())
        if resposta is "n": break
    tcp.close()


main()
