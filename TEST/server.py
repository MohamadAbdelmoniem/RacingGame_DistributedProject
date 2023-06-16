import socket
import threading
import pickle

SERVER_IP = "localhost"
SERVER_PORT = 5550

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((SERVER_IP, SERVER_PORT))
except socket.error as e:
    print(str(e))

server.listen(3)
print("Waiting for a connection, Server Started")

scores = {"player1": 0, "player2": 0}
positions = {"player1": (330,400), "player2": (330,400)}
clients = []

def broadcast(msg):
    for client in clients:
        client.sendall(pickle.dumps(msg))

def chat_handler(conn):
    while True:
        try:
            chat_msg = pickle.loads(conn.recv(2048))
            if not chat_msg:
                break
            if chat_msg.get('chat'):
                broadcast(chat_msg)
        except:
            break

def threaded_client(conn, player_id):
    print("server will send id: ", player_id)
    conn.send(pickle.dumps(player_id))
    print("server sent id: ", player_id)

    chat_thread = threading.Thread(target=chat_handler, args=(conn,))
    chat_thread.start()

    while True:
        try:
            print("received data")
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("no data")
                print("Disconnected")
                break
            else:
                player_key = "player" + str(player_id + 1)
                opponent_key = "player" + str((player_id + 1) % 2 + 1)
                scores[player_key], positions[player_key] = data
                conn.sendall(pickle.dumps(scores))
                conn.sendall(pickle.dumps(positions))

                print("Received: ", data)
                print("Sending : ", scores)

        except:
            break

    print("Lost connection")
    conn.close()
    clients.remove(conn)
    print("newClientsAfterRemoval: ", clients)

currentPlayer = 0
connectedPlayers = 0
while True:
    conn, addr = server.accept()
    print("Connected to:", addr)
    clients.append(conn)
    print("newClientsAfterAppending: ", clients)
    connectedPlayers += 1
    thread = threading.Thread(target=threaded_client, args=(conn, currentPlayer))
    thread.start()
    currentPlayer += 1
    if currentPlayer > 1:
        currentPlayer = 0