#Import for online
import socket

#Imports for game
import random as r
import time as t
import operator as o

#Variables
Colors = ["R", "G", "B", "Y"]
Values = ["", "D", "D2", "D2", "S", "S", "R", "R", "0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9"]
PlayerList = []

TopCard = Card(Colors[r.randrange(0, 3)], Values[r.randrange(0, 26)])
while TopCard.Value in Values[0:7]:
    TopCard = Card(Colors[r.randrange(0, 3)], Values[r.randrange(0, 26)])

GameOver = False
Reverse = False

Stacking = 0
NumberOfPlayers = 0

while True:
    try:
        NumberOfPlayers = int(input("How many players? 2-20 >>> "))
        if NumberOfPlayers < 2:
            raise ValueError
        break
    except ValueError:
        print("Not in range... try again")
        pass

#Define top-level functions
def SendToAll(Message):
    global NumberOfPlayers
    i = 0
    for i in range(NumberOfPlayers): #Repeat for each player
        PlayerList[i].SendTo(Message) #Use the Player objects funciton to send a message to the client
        i = i + 1 #Next player

def CardOut(List):
    TempList,i = [],0
    while i in range(len(List)):
        TempList.append(List[i].Output) #Add the output of the card to the templist
        i = i + 1
    return TempList #Output all Card.Outputs from the list
        
#Classes
class Card:    
    def __init__(self, Color, Value):
        self.Color = Color #Str
        self.Value = Value #Str
        self.Output = ''.join([Color, Value]) #Str

class Player:
    def Draw(Number):
        global Colors, Values
        for _ in range(Number):
            Draw = Card(r.sample(Colors, 1)[0], r.sample(Values, 1)[0]) #Make a random card
            if Card.Value in ["", "D"]:
                Draw.Color = "W"
                Draw.Output = ''.join([Draw.Color, Draw.Value])
            self.Hand.append(Draw)
        if Number not in [1, 7]:
            SendToAll(''.join(["\n", self.Name, "had to draw", Number, "cards."])) #Send the output to everyone
        return True

    def SendTo(Message):
        self.Socket.send(Message.encode())
    
    def __init__(self, Name, Hand, Socket):
        self.Name = Name #Str
        self.Hand = self.Draw(7) #Lst
        self.Socket = Socket #???

#Main game functions
def Turn(Player, Turn):
    global Colors, PlayerList, TopCard, GameOver, Reverse, Stacking, NumberOfPlayers

    #Define
    Skip = False
    Ops = {False: o.add, True: o.sub}
    Usable,Ints = [],[]
    i = 0

    #Add usable cards into Usable
    while i in range(len(Player.Hand)):
        if Player.Hand[i].Color == TopCard.Color or Player.Hand[i].Value == TopCard.Value or Player.Hand[i].Value in ["", "D"]:
            Usable.append(Player.Hand[i])
            Ints.append(i)
        i = i + 1

    #Info
    SendToAll(''.join(["\n", Player.Name, "'s turn!", "\n", Player.Name, " has ", str(len(Player.Hand)), " cards.|Print"]))

    if len(Usable) > 0:
        Player.SendTo(''.join(["Current card:", TopCard.Output, "\nYour cards:", CardOut(Player.Hand), "\nYour usable cards:", CardOut(Usable), "|Print"]))
        while True:
            try:
                Player.SendTo(''.join(["What card are you going to play? 1-", str(len(Usable)), " >>> |Input"]))
                Input = int(int(Player.Socket.recv(1024).decode()) - 1)
                if Input <= len(Usable):
                    break
                else:
                    pass
            except (ValueError, IndexError):
                Player.SendTo("Not in range... try again|Print")
                pass

        TopCard = Usable[Input]

        #Special cards
        if Usable[Input].Value in ["", "D"]:
            while True:
                try:
                    Player.SendTo("What color? (R/G/B/Y) >>> |Input")
                    Color = Player.Socket.recv(1024).decode().lower()
                    if Color.count("r") > 0:
                        Color = "R"
                    elif Color.count("g") > 0:
                        Color = "G"
                    elif Color.count("b") > 0:
                        Color = "B"
                    elif Color.count("y") > 0:
                        Color = "Y"
                    else:
                        raise ValueError
                    TopCard.Color = Color
                    break
                except(ValueError, IndexError):
                    Player.SendTo("Not a valid input... try again|Print")
                    pass
        if Usable[Input] == "D":
            try:
                Skip = PlayerList[int(Ops[Reverse](Turn, 1))].Draw(4)
            except IndexError:
                if Reverse:
                    Skip = PlayerList[-1].Draw(4)
                else:
                    Skip = PlayerList[0].Draw(4)
        if Usable[Input] == "D2":
            try:
                Skip = PlayerList[int(Ops[Reverse](Turn, 1))].Draw(2)
            except IndexError:
                if Reverse:
                    Skip = PlayerList[-1].Draw(2)
                else:
                    Skip = PlayerList[0].Draw(2)
        if Usable[Input] == "S":
            Skip = True
        if Usable[Input] == "R":
            Reverse = not Reverse

        Player.Hand.pop(Ints[Input])

    elif len(Player.Hand) == 0:
        SendToAll(''.join(["The winner is", Player.Name, "!|Print"]))
        GameOver = True
    
    elif len(Usable) == 0:
        SendToAll(''.join([Player.Name, "Has no usable cards... they will draw and be skipped|Print"]))
        Player.Draw(1)

    Turn = Ops[Reverse](Turn, 1)
    if Skip:
        Turn = Ops[Reverse](Turn, 1)
        Skip = False

    if Turn == int(NumberOfPlayers):#looping to make the game be longer than NumberOfPlayers turns
        Turn = 0
    if Turn == int(NumberOfPlayers + 1):
        Turn = 1
            
    if Turn == -1:
        Turn = int(NumberOfPlayers - 1)
    if Turn == -2:
        Turn = int(NumberOfPlayers - 2)

    #Return
    return Turn

def Game():
    global PlayerList, GameOver
    Next = 0
    while not GameOver:
        Next = Turn(PlayerList[Next], Next)

#Set up server
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Host = (socket.gethostname(), 5001)
ServerSocket.bind(Host)

ServerSocket.listen(NumberOfPlayers)
i = 0
while i in range(NumberOfPlayers):
    ClientSocket, Address = ServerSocket.accept()
    ClientSocket.send("What Is Your Name? >>> |Input".encode())
    Temp = Player(ClientSocket.recv(1024).decode(), [], Address, ClientSocket)
    Temp.Draw(7)
    PlayerList.append(Temp)
    i = i + 1
Game()
socket.shutdown()
socket.close()
