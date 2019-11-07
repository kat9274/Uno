from socket import *
from multiprocessing import Process
Socket = socket()

def Start(Port):
    try:
        Socket.bind(('', Port))
        Socket.listen()
        print(f"Listening...")
        return 0
    except Exception as e:
        print(f"ConnectionError: {e.__class__.__name__} in Start()")
        return 1

def Connect():
    try:
        C, A = Socket.accept()
        print(f"{A[0]} connected.")
        return C
    except Exception as e:
        print(f"ConnectionError: {e.__class__.__name__}")

def Send(C, Message):
    try:
        if __name__ == f"__main__":
            P = Process(target=C.send, args=(f"{Message}".encode(), ))
            P.start() #Start the process
            P.join() #Wait to finish
        return 0
    except Exception as e:
        print(f"ConnectionError: {e.__class__.__name__}")

def Get(C):
    try:
        Message = C.recv(4096).decode()
        return Message
    except Exception as e:
        print(f"ConnectionError: {e.__class__.__name__}")
