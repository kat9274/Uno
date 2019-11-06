from socket import *
Socket = socket()

class Connect:
    def __init__(self):
        try:
            self.C, self.Address = Socket.accept()
            print(self.Address[0], "connected.")
        except Exception as e:
            print("ConnectionError: ", str(e.__class__.__name__))
            return 1

    def Send(self, Message):
        try:
            self.C.send(str(Message).encode())
            return 0
        except Exception as e:
            print("ConnectionError: ", str(e.__class__.__name__))
            return 1
            

    def Get(self):
        try:
            Message = self.C.recv(4096).decode()
            return Message
        except Exception as e:
            print("ConnectionError: ", str(e.__class__.__name__))
            return 1
        
def Start(Port):
    try:
        Port = Port
        Socket.bind(('', Port))
        Socket.listen()
        print("Listening...")
        return 0
    except Exception as e:
        print("ConnectionError: ", str(e.__class__.__name__))
        return 1
