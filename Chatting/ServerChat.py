import socket
import threading

PRIMARY_SERVER_IP = 'localhost'
PRIMARY_SERVER_PORT = 12000
BACKUP_SERVER_IP = 'localhost'
BACKUP_SERVER_PORT = 12001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((PRIMARY_SERVER_IP, PRIMARY_SERVER_PORT))
server.listen()

clients = []
nicknames = []

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
            nicknames.remove(nickname)
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            break

def accept_connections():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Primary server is listening...")
accept_connections()