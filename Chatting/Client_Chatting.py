import socket
import threading
from tkinter import *

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                text_box.config(state=NORMAL)
                text_box.insert(END, message + "\n")
                text_box.config(state=DISABLED)
        except:
            print("Error")
            client.close()
            break

def send(event=None):
    message = f'{nickname}: {input_msg.get()}'
    client.send(message.encode('utf-8'))
    input_msg.set('')

def on_closing(event=None):
    input_msg.set('!quit')
    send()
    window.quit()

PRIMARY_SERVER_IP = '127.0.0.1'
PRIMARY_SERVER_PORT = 5000
BACKUP_SERVER_IP = '127.0.0.1'
BACKUP_SERVER_PORT = 6000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((PRIMARY_SERVER_IP, PRIMARY_SERVER_PORT))
except:
    print("Primary server is down. Connecting to the backup server...")
    client.connect((BACKUP_SERVER_IP, BACKUP_SERVER_PORT))

window = Tk()
window.title("Chat Client")

frame = Frame(window)
scrollbar = Scrollbar(frame)
text_box = Text(frame, height=15, width=50, yscrollcommand=scrollbar.set, state=DISABLED)
scrollbar.pack(side=RIGHT, fill=Y)
text_box.pack(side=LEFT, fill=BOTH)
frame.pack()

input_msg = StringVar()
input_msg.set('')
input_field = Entry(window, text=input_msg, width=50)
input_field.bind('<Return>', send)
input_field.pack()

send_button = Button(window, text='Send', command=send)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

nickname = input("Enter your nickname: ")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

window.mainloop()