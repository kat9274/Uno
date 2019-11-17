from socket import *
Socket = socket()
PrintErrors = True


def Connect(Host, Port):
    try:
        Socket.connect((Host, Port))
        return 0
    except Exception as e:
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")
        return 1


def Send(Message):
    try:
        Socket.send(f"{Message}".encode())
        return 0
    except Exception as e:
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")
        return 1


def Get():
    try:
        Message = Socket.recv(4096).decode()
        return Message
    except Exception as e:
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")
        return 1
