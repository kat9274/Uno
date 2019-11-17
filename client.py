from socket import *
Socket = socket() #Start the socket
PrintErrors = True #Print out the errors


def Connect(Host, Port):
    try:
        Socket.connect((Host, Port)) #Connect to the provided adress
        return 0
    except Exception as e: #Print the error if PrintErrors == True
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")
        return 1


def Send(Message):
    try:
        Socket.send(f"{Message}".encode()) #Send message to server
        return 0
    except Exception as e: #Print the error if PrintErrors == True
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")
        return 1


def Get():
    try:
        Message = Socket.recv(4096).decode() #Get and return message from server
        return Message
    except Exception as e: #Print the error if PrintErrors == True
        if PrintErrors:
            print(f"ConnectionError: {e.__class__.__name__}")
        return 1
