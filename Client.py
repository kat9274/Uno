import socket, json

while True:
    try:
        Server = "192.168.1.100" #input("What IP do you want to connect to? >>> ")
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

while Recive[1] != "GameOver":
    Recive = ClientSocket.recv(1024).decode()
    Recive = Recive.split("|")
    if Recive[1] == "Input":
        ClientSocket.send(input(Recive[0]).encode())
    elif Recive[1] == "Print":
        print(Recive[0])
        
print(Recive[0])    
ClientSocket.close()  #Close the connection after the server sends "GameOver"
