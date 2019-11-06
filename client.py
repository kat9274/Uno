from socket import *
Socket = socket()

def Send(Message):
    try:
        Socket.send(str(Message).encode())
        return 0
    except Exception as e:
        print("ConnectionError:", str(e.__class__.__name__))
        return 1

def Get():
    try:
        Message = Socket.recv(4096).decode()
        return Message
    except Exception as e:
        print("ConnectionError:", str(e.__class__.__name__))
        return 1

def Connect(Host, Port):
    try:
        Socket.connect((Host, Port))
        return 0
    except Exception as e:
        print("ConnectionError: ", str(e.__class__.__name__))
        return 1
