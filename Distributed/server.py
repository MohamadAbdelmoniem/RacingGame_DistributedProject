import socket
from _thread import *
import random
import pygame
from player import PlayerVehicle , PlayerVehiclez
import pickle
import numpy as np

server="localhost"
port = 5550

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))

s.listen(3)
print("Waiting for a connection, Server Started")

score=[0,0,0]
'''scores of players = [p1,p2,p3]'''

def threaded_client(conn,player_id):
    print("server will send id: ",player_id)
    conn.send(pickle.dumps(player_id)) # sending player id to connected  client
    print("server sent id: ",player_id)
    reply=''

    while player_id < 1:
        pass
    while True:
        try:
            print("received data")
            data = pickle.loads(conn.recv(2048)) #receiving score
            score[player_id] = data # updating player score in server

            if not data:
                print("no data")
                print("Disconnected")
                break
            else: # choosing client to send score to
                print("data found")
                if player_id == 1:
                    reply = score[0]
                else:
                    reply = score[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply)) #sending updated score to desired client
        except:
            break

    print("Lost connection")
    conn.close()
    
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    if currentPlayer>2:
        currentPlayer=0