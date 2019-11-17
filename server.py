from socket import *
from sys import *
from multiprocessing import Process
Socket = socket() #Start socket
PrintErrors = True #Print out the errors


def Start(Port):
    try:
        Socket.bind(('', Port)) #Bind the port
        Socket.listen() #listen for connections
        print(f"Listening...")
        return 0
    except Exception as e: #Print the error if PrintErrors == True
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__} in Start()")


def Connect():
    try:
        C, A = Socket.accept() #Accept the connection and return it
        print(f"{A[0]} connected.")
        return C
    except Exception as e: #Print the error if PrintErrors == True
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")


def Send(C, Message):
    try:
        P = Process(target=C.send, args=(f"{Message}".encode(), )) #Send to connection
        P.start()  # Start the process
        P.join()  # Wait to finish
        return 0
    except Exception as e: #Print the error if PrintErrors == True
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")


def Get(C):
    try:
        Manager = Manager() #IDK (Copied from stackoverflow)
        Return = Manager.dict() #IDK
        P = Process(target=C.recv(), args(4096, )) #Get
        P.start()
        P.join()
        return Return.values().decode() #Returns what you get?
    except Exception as e: #Print the error if PrintErrors == True
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")
