import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.102"
        self.port = 5550
        self.addr = (self.server, self.port)
        self.player_id = self.connect()
        print("here 1")

    def getPLayer_id(self):
        return self.player_id

    def connect(self): # connects to the server and server receives player id from server
        try:
            self.client.connect(self.addr)
            print("here")
            return pickle.loads(self.client.recv(2048)) 
        except:
            pass

    def send(self, data):
        try:
            print("sending player 2")
            self.client.send(pickle.dumps(data)) # sending score
            print("player 2 sent")
            return pickle.loads(self.client.recv(2048)) # receiving score for other players
        except socket.error as e:
            print(e)