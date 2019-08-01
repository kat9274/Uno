#Imports for networking
import socket
from threading import *

#Imports for game
import random as r
import time as t
import operator as o

#Define variables for game
class Player:
    def __init__(self, Name, Hand, IP, Socket):
        self.Name = Name #Str
        self.Hand = Hand #Lst
        self.IP = IP #???
        self.Socket = Socket #???

class Card:
    def __init__(self, Color, Value):
        self.Color = Color #Str
        self.Value = Value #Str
        self.Output = "".join([Color, Value]) #Str

    #Lists
Colors = ["R", "G", "B", "Y"]
Values = ["", "D", "D2", "D2", "S", "S", "R", "R", "0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9"]
PlayerList = []
    #TopCard
TopCard = Card(Colors[r.randrange(0, 3)], Values[r.randrange(0, 26)])
while TopCard.Value in Values[0:7]:
    TopCard = Card(Colors[r.randrange(0, 3)], Values[r.randrange(0, 26)])
    #Bools
GameOver = False
Reverse = False
    #Ints
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

#Define functions
def SendToAll(Message):
    global NumberOfPlayers
    i = 0
    while i in range(NumberOfPlayers):
        PlayerList[i].Socket.send(Message.encode())
        i = i + 1

def Draw(Player, Number):
    global Colors, Values, PlayerList, TopCard, GameOver, Reverse, Stacking, NumberOfPlayers
    for _ in range(Number): #The _ is a variable that you dont need to increment
        Draw = Card(r.sample(Colors, 1)[0], r.sample(Values, 1)[0]) #Generate a card to output
        if Draw.Value in ["", "D"]: #If the card is Wild set it to wild
            Draw.Color = "W"
            Draw.Output = "".join([Draw.Color, Draw.Value]) #Reset the output as it got messed up
        Player.Hand.append(Draw) #Append the object "Draw" to Player.Hand
    if Number not in [1, 7]:
        SendToAll(''.join([''.join(["\n", Player.Name, "Had to draw", Number, "cards."]), "|Print"]))
    return True #Reduces lines by 2 and makes code more simple

def CardOut(List):
    global Colors, Values, PlayerList, TopCard, GameOver, Reverse, Stacking, NumberOfPlayers
    TempList,i = [],0
    while i in range(len(List)):
        TempList.append(List[i].Output)
        i = i + 1
    return TempList #Output all Card.Outputs from the list

def Turn(Player, Turn):
    global Colors, Values, PlayerList, TopCard, GameOver, Reverse, Stacking, NumberOfPlayers

    #Define
    Skip,Do = False,True
    Ops = {False: o.add, True: o.sub}
    Usable = []
    Ints = []
    i = 0

    #Add All PlayAble Cards Into PlayAble Cards And Get Rid of Playable cards In UnPlayAbleCards
    while i in range(len(Player.Hand)):
            if Player.Hand[i].Color == TopCard.Color or Player.Hand[i].Value == TopCard.Value or Player.Hand[i].Value in ["", "D"]:
                Usable.append(Player.Hand[i])
                Ints.append(i)
            i = i + 1

    #Info
    SendToAll(''.join(["\n", Player.Name, "'s turn!", "\n", Player.Name, " has ", str(len(Player.Hand)), " cards.", "|Print"]))
    
    if len(Usable) > 0:   
        Player.Socket.send(''.join(["Current card:", TopCard.Output, "\nYour cards:", CardOut(Player.Hand), "\nYour usable cards:", CardOut(Usable), "|Print"]))
        while True:
            try:
                Player.Socket.send("".join(["What Card Are You Going To Play? 1-", str(len(Usable)), " >>> ", "|Input"]))#Get The Card That Is Going To Be Played
                Input = Player.Socket.recv(1024).decode()
                if Input <= len(Usable):
                    break
                else:
                    pass
            except ValueError:
                pass
            except IndexError:
                pass

        if Do:
            TopCard = Usable[Input]

        #Special Cards
        if Usable[Input].Value in ["", "D"]:
            while True:
                try:
                    Player.Socket.send(''.join(["What color? (R/G/B/Y) (Need to be exact) >>> ", "|Input"]))
                    TopCard.Color = Player.Socket.recv(1024).decode()
                    if TopCard.Color not in Colors:
                        pass
                    else:
                        TopCard.Output = [TopCard.Color, TopCard.Value]
                        break
                except (ValueError, IndexError):
                    pass
                
        if Usable[Input].Value == "D":
            try:
                Skip = Draw(PlayerList[int(Ops[Reverse](Turn, 1))], 4)
            except IndexError:
                if Reverse:
                    Skip = Draw(PlayerList[NumberOfPlayers], 4)
                else:
                    Skip = Draw(PlayerList[0], 4)
        if Usable[Input].Value == "D2":
            try:
                Skip = Draw(PlayerList[int(Ops[Reverse](Turn, 1))], 2)
            except IndexError:
                if Reverse:
                    Skip = Draw(PlayerList[NumberOfPlayers], 2)
                else:
                    Skip = Draw(PlayerList[0], 2)
        if Usable[Input].Value == "S":
            Skip = True
        if Usable[Input].Value == "R":
            Reverse = not Reverse
                        
        if Do:
            Player.Hand.pop(Ints[Input])

    elif len(Usable) == 0:
        SendToAll(''.join([Player.Name, "Has no usable cards... they will draw and be skipped", "|Print"])) #If The Player Has No Cards Draw And Skip Them
        Draw(Player, 1)
        
    if len(Player.Hand) == 0: #If a Player Has 0 Cards They Win
        SendToAll(''.join(["The Winner Is", Player.Name, "!", "|Print"]))
        GameOver = True
    
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
    global Colors, Values, PlayerList, TopCard, GameOver, Reverse, Stacking, NumberOfPlayers
    Next = 0
    while not GameOver:
        Next = Turn(PlayerList[Next], Next)

#Set up server
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Host = socket.gethostname()
Port = 5000
ServerSocket.bind((Host, Port))

ServerSocket.listen(NumberOfPlayers)
i = 0
while i in range(NumberOfPlayers):
    ClientSocket, Address = ServerSocket.accept()
    ClientSocket.send("What Is Your Name? >>> |Input".encode())
    Temp = Player(ClientSocket.recv(1024).decode(), [], Address, ClientSocket)
    Draw(Temp, 7)
    PlayerList.append(Temp)
    i = i + 1
Game()
Connection.close()  # close the connection
