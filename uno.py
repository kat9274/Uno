from client import *

def Parse():
    global GameOver
    Message = Get().decode().split('`')
    print(f"{Message[0]}")
    if Message[1] == 'y':
        Send(f"{input(f'{Message[2]}')}")
    elif Message[1] == 'g':
        GameOver = True

while True:
    Status = Connect(input(f"Server >>> "), 9274)
    if Status == 0:
        print(f"Connected.")
        break

GameOver = False
while not GameOver:
    Parse()
