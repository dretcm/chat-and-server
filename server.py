import socket # used for the network connection
import threading # necessary for performing various tasks at the same time
import sys

#host = '127.0.0.1' # equals to 0.0.0.0
host = '192.168.1.8' # local or lan
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients = [0]
nicknames = [0]

clients.clear()
nicknames.clear()


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        try:
            client, address = server.accept()
            print("Connected with {}".format(str(address)))

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print("Nickname is {}".format(nickname))
            broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            sys.exit(1)
            

print('Server in action .........')
receive()
server.close()