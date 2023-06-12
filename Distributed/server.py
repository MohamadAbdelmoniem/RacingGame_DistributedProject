import socket
import threading
import random
import pygame
from player import PlayerVehicle, PlayerVehiclez
import pickle
import numpy as np

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

clients = []


def broadcast(scores):
    for client in clients:
        conn.send_json(scores)


def threaded_client(conn, player_id):

    print("server will send id: ", player_id)
    conn.send(pickle.dumps(player_id))  # sending player id to connected  client
    print("server sent id: ", player_id)
    reply = ""
    while True:
        try:
            print("received data")
            data = pickle.loads(conn.recv(2048))  # receiving score
            if ("player" + str(player_id + 1)) in scores.keys():
                scores[
                    "player" + str(player_id + 1)
                ] = data  # updating player score in server

            if not data:
                print("no data")
                print("Disconnected")
                break
            else:
                """broadcast(scores)"""
                conn.sendall(pickle.dumps(data))

                print("Received: ", data)
                print("Sending : ", scores)

            # sending updated score to desired client
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
