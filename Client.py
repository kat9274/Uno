import socket, json

while True:
    try:
        Server = input("What IP do you want to connect to? >>> ")
        Port = 5000
        
        ClientSocket = socket.socket()
        ClientSocket.connect((Server, Port))
        break
    except ConnectionRefusedError:
        print("Server not running... try again")
        pass
    except socket.gaierror:
        print("Not a valid ip... try again")
        pass

Recive = ["", "", ""]

while Recive[0] != "GameOver":
    Recive = ClientSocket.recv(1024).decode()
    Recive = Recive.split(",")
    if Recive[0] == socket.gethostbyname(socket.gethostname()):
        if Recive[2] == "Input":
            ClientSocket.send(input(Recive[1]).encode())
        elif Recive[2] == "Print":
            print(Recive[1])
        
print(Recive[1])    
ClientSocket.close()  #Close the connection after the server sends "GameOver"
