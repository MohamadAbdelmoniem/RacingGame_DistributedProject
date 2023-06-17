def create_Chat():
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
    PRIMARY_SERVER_PORT = 5553


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    client1.connect((PRIMARY_SERVER_IP, PRIMARY_SERVER_PORT))
    
    from tkinter import Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, Tk, StringVar, DISABLED, NORMAL, RIGHT, LEFT, Y, W, E, S, N, BOTH

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

def options():
    game_thread = threading.Thread(target=run_game_loop)
    game_thread.start()
    
    create_Chat()

def run_game_loop():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()