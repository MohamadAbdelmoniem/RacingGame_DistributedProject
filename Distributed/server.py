import socket
import threading
import pickle
from pymongo.mongo_client import MongoClient


SERVER_IP = "localhost"
SERVER_PORT = 5550
CHAT_SERVER_PORT = 5551

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    server.bind((SERVER_IP, SERVER_PORT))
except socket.error as e:
    print(str(e))

server.listen(3)
print("Waiting for a connection, Server Started")

scores = {"player1": 0, "player2": 0}

clients = []
####################################--DB--##############################################################
uri = "mongodb+srv://karim:karim@cluster0.mqdt2q9.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
gameDB = client.game
playerCollection = gameDB.player



def update_player_db(score,speed,unique_id):
    from bson.objectid import ObjectId

    _id = ObjectId(unique_id)
    updates = {
        "$set": {"score":score,"speed":speed}
    }
    playerCollection.update_one({"_id":_id},updates)


def create_doc(player_id):
    doc = {
        "player_id":player_id,
        "speed": 0,
        "score": 0
    }
    inserted_id = playerCollection.insert_one(doc).inserted_id
    return inserted_id




def broadcast(scores):
    for client in clients:
        conn.send_json(scores)


def threaded_client(conn, player_id,unique_id):

    print("server will send id: ", player_id)
    conn.send(pickle.dumps(player_id))  # sending player id to connected  client
    print("server sent id: ", player_id)
    reply = ""
    while True:
        try:
            print("received data")
            score = pickle.loads(conn.recv(2048))  # receiving score
            speed = pickle.loads(conn.recv(2048))
            if ("player" + str(player_id + 1)) in scores.keys():
                scores[
                    "player" + str(player_id + 1)
                ] = score  # updating player score in server

                update_player_db(score,speed,unique_id)


            if not score:
                print("no data")
                print("Disconnected")
                break
            else:
                """broadcast(scores)"""
                '''conn.sendall(pickle.dumps(data))'''
                if player_id == 0:
                    conn.sendall(pickle.dumps(scores["player2"]))
                else:
                    conn.sendall(pickle.dumps(scores["player1"]))

                print("Received: ", score)
                print("Sending : ", scores)

            # sending updated score to desired client
        except:
            break

    print("Lost connection")
    conn.close()
    scores["player" + str(player_id + 1)] = 0
    clients.remove(conn)
    print("newClientsAfterRemoval: ", clients)


currentPlayer = 0
connectedPlayers = 0
while True:
    conn, addr = server.accept()
    print("Connected to:", addr)
    clients.append(conn)
    unique_id = create_doc(currentPlayer)
    print("newClientsAfterAppending: ", clients)
    connectedPlayers += 1
    thread = threading.Thread(target=threaded_client, args=(conn, currentPlayer,unique_id))
    thread.start()
    currentPlayer += 1
    if currentPlayer > 1:
        currentPlayer = 0