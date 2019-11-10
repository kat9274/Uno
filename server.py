from socket import *
from sys import *
from multiprocessing import Process
Socket = socket()
PrintErrors = True

def Start(Port):
    try:
        Socket.bind(('', Port))
        Socket.listen()
        print(f"Listening...")
        return 0
    except Exception as e:
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__} in Start()")

def Connect():
    try:
        C, A = Socket.accept()
        print(f"{A[0]} connected.")
        return C
    except Exception as e:
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")

def Send(C, Message):
    try:
        P = Process(target=C.send, args=(f"{Message}".encode(), ))
        P.start() #Start the process
        P.join() #Wait to finish
        return 0
    except Exception as e:
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")

def Get(C):
    try:
        Manager = Manager()
        Return = Manager.dict()
        P = Process(target=C.recv(), args(4096, ))
        P.start()
        P.join()
        return Return.values().decode()
    except Exception as e:
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")
