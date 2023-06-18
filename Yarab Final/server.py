import socket
import threading
import pickle
from pymongo.mongo_client import MongoClient


SERVER_IP = "172.31.27.84"
SERVER_PORT = 5552
chat_port = 5553

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((SERVER_IP, SERVER_PORT))
    server1.bind((SERVER_IP, chat_port))
except socket.error as e:
    print(str(e))

server.listen(3)
server1.listen()


scores = {"player1": 0, "player2": 0}
positions = {"player1": (330,400), "player2": (330,400)}
speeds = {"player1":0,"player2":0}
quits = {"player1":0,"player2":0}
clients = []
nicknames = []
clients1 = []
dict = {}

##########################################--DB--###################################################
uri = "mongodb+srv://karim:karim@cluster0.mqdt2q9.mongodb.net/?retryWrites=true&w=majority"
DB_Client = MongoClient(uri)
gameDB = DB_Client.game
playerCollection = gameDB.player

def update_doc(player_key,score,speed,position):

    doc = {
        "$set":{"score":score,
                "speed":speed,
                "positions":position
                }
    }
    playerCollection.update_one({"player_id":player_key},doc)

def reset_doc(player_key):

    doc = {
        "$set":{"score":0,
                "speed":2,
                "positions":(330,400)
                }
    }
    playerCollection.update_one({"player_id":player_key},doc)


def read_score(player_key):
    query = {"player_id": player_key}
    player = playerCollection.find_one(query)
    player_score = player["score"]
    return player_score

def read_speed(player_key):
    query = {"player_id": player_key}
    player = playerCollection.find_one(query)
    player_speed = player["speed"]
    return player_speed
    

def read_position(player_key):
    query = {"player_id": player_key}
    player = playerCollection.find_one(query)
    player_pos = player["positions"]
    return player_pos

def init_dicts(player_key):
    scores[player_key] = read_score(player_key)
    speeds[player_key] = read_speed(player_key)
    positions[player_key] = tuple(read_position(player_key))

def broadcast(scores):
    for client in clients:
        client.sendall(pickle.dumps(scores))

def broadcast1(message):
    for client in clients1:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast1(message)
        except:
            index = clients.index(client)
            clients1.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast1(f'{nickname} left the chat!'.encode('utf-8'))
            break

def threaded_client(conn, player_id):
    print("server will send id: ", player_id)
    conn.send(pickle.dumps(player_id))
    print("server sent id: ", player_id)
    init_dicts("player" + str(player_id + 1))
    dict1 = {
        "scores": list(scores.values()),
        "speeds": list(speeds.values()),
        "positions": list(positions.values()),
        "quits" : list(quits.values())
    }
    
    
    conn.send(pickle.dumps(dict1)) #sending dict

    while True:
        try:
            
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break
            else:
                player_key = "player" + str(player_id + 1)
                opponent_key = "player" + str((player_id + 1) % 2 + 1)
                scores[player_key], speeds[player_key],positions[player_key],quits[player_key] = data
                if quits[player_key]==1:
                    reset_doc(player_key)
                

                update_doc(player_key,scores[player_key],speeds[player_key],positions[player_key])
                print("scores: ", scores)
                print("positions: ", positions)
                dict ={
                    "scores": list(scores.values()),
                    "speeds": list(speeds.values()),
                    "positions": list(positions.values()),
                    "quits" : list(quits.values())
                }
                broadcast(dict)

                #conn.sendall(pickle.dumps(scores,positions))
                #conn.sendall(pickle.dumps(positions))



        except:
            break
    if quits[player_key]==1:
        reset_doc(player_key)
    

    
    conn.close()
    clients.remove(conn)
    

currentPlayer = 0
connectedPlayers = 0
def game_server():
    global currentPlayer
    global connectedPlayers
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        connectedPlayers += 1
        thread = threading.Thread(target=threaded_client, args=(conn, currentPlayer))
        thread.start()
        currentPlayer += 1
        if currentPlayer > 1:
            currentPlayer = 0
def chat_server():
    while True:
        client, address = server1.accept()

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients1.append(client)

        broadcast1(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))
        thread1 = threading.Thread(target=handle, args=(client,))
        thread1.start()
# Start game_server and chat_server in separate threads
game_server_thread = threading.Thread(target=game_server)
chat_server_thread = threading.Thread(target=chat_server)

game_server_thread.start()
chat_server_thread.start()

game_server_thread.join()
chat_server_thread.join()

