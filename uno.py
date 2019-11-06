from client import *

GameOver = False

def Parse():
    global GameOver
    Message = Get().split('`')
    print(Message[0])
    if Message[1].lower() == "y":
        Send(input(Message[2]))
    elif Message[1].lower() == "GameOver":
        GameOver = True
    return Message

while True:
    Host = str(input("Server Ip >>> "))
    Status = Connect(Host, 9274)
    if Status == 0:
        print("Connected.")
        break

while not GameOver:
    Parse()
