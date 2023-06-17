import socket
import threading
import pickle
from pymongo.mongo_client import MongoClient

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
speeds = {"player1":0,"player2":0}
quits = {"player1":0,"player2":0}
clients = []
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
    print("dict1",dict1)
    
    conn.send(pickle.dumps(dict1)) #sending dict

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
                scores[player_key], speeds[player_key],positions[player_key],quits[player_key] = data
                if quits[player_key]==1:
                    reset_doc(player_key)
                    print("reset")

                update_doc(player_key,scores[player_key],speeds[player_key],positions[player_key])
                print("scores: ", scores)
                print("positions: ", positions)
                dict ={
                    "scores": list(scores.values()),
                    "speeds": list(speeds.values()),
                    "positions": list(positions.values()),
                    "quits" : list(quits.values())
                }
                print(dict)
                broadcast(dict)

                #conn.sendall(pickle.dumps(scores,positions))
                #conn.sendall(pickle.dumps(positions))

                print("Received: ", data)
                print("Sending : ", dict)

        except:
            break
    if quits[player_key]==1:
        reset_doc(player_key)
        print("reset")    

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