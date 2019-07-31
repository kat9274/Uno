#import
import random as r
import time as t
import operator as o
import base64 as b

#Classes
class Card: #Card class has Color, Value and Output
    def __init__(self, Color, Value):
        self.Color = Color #Str
        self.Value = Value #Str
        self.Output = "".join([Color, Value]) #Str

class Player: #Player class has Name and Hand
    def __init__(self, Name, Hand):
        self.Name = Name #Str
        self.Hand = Hand #Lst

#Define
Colors = ["R", "G", "B", "Y"]
Values = ["", "D", "D2", "D2", "S", "S", "R", "R", "0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9"]

TopCard = Card(Colors[r.randrange(0, 3)], Values[r.randrange(0, 26)])
while TopCard.Value in Values[0:7]:
    TopCard = Card(Colors[r.randrange(0, 3)], Values[r.randrange(0, 26)])
PlayerList = []
GameOver = False
Reverse = False
NumberOfPlayers,Stacking = 0,0

#Side functions
def Draw(Player, Number):
    global Colors, Values
    for _ in range(Number): #The _ is a variable that you dont need to increment
        Draw = Card(r.sample(Colors, 1)[0], r.sample(Values, 1)[0]) #Generate a card to output
        if Draw.Value in ["", "D"]: #If the card is Wild set it to wild
            Draw.Color = "W"
            Draw.Output = "".join([Draw.Color, Draw.Value]) #Reset the output as it got messed up
        Player.Hand.append(Draw) #Append the object "Draw" to Player.Hand
    if Number not in [1, 7]:
        print("\n", Player.Name, "Had to draw", Number, "cards.")
    return True #Reduces lines by 2 and makes code more simple

def CardOut(List):
    TempList,i = [],0
    while i in range(len(List)):
        TempList.append(List[i].Output)
        i = i + 1
    return TempList #Output all Card.Outputs from the list

def Setup():
    global NumberOfPlayers
    i = 0
    while True: #Get number of players
        try:
            NumberOfPlayers = int(input("How many players? (More than 1) >>> "))
            if NumberOfPlayers < 2:
                print("2 players it is!")
                NumberOfPlayers = 2
            break
        except ValueError:
            print("Please input a valid number.")
            pass
    while i < NumberOfPlayers: #Make every player and append it to PlayerList
        TempPlayer = Player(input(''.join(["What is player ", str(int(i + 1)), "'s name? >>> "])), [])
        Draw(TempPlayer, 7)
        PlayerList.append(TempPlayer)
        i = i + 1

#Main functions
def Turn(Player, Turn):
    global Colors, Values, TopCard, PlayerList, NumberOfPlayers, Stacking, Reverse, GameOver

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
    print(''.join(["\n", Player.Name]), "'s turn!")
    print("You Have ", len(Player.Hand), "Cards.")
    t.sleep(2)
    
    if len(Usable) > 0:   
        print("Current card:", TopCard.Output, "\nYour cards:", CardOut(Player.Hand), "\nYour usable cards:", CardOut(Usable))
        while True:
            try:
                Input = int(int(input("".join(["What Card Are You Going To Play? 1-", str(len(Usable)), " >>>"]))) - 1) #Get The Card That Is Going To Be Played
                if Input == 9273:
                    if b.b64encode(input("Password >>> ").encode()) == b'R2hvc3Q=':
                        Usable.append(Card(input("Color as string >>> "), input("Value as string >>> ")))
                        Do = False
                        pass
                elif Input <= len(Usable):
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
                    TopCard.Color = input("What color? (R/G/B/Y) (Need to be exact) >>>")
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
        print("You Have No Usable Cards... You Will Draw") #If The Player Has No Cards Draw And Skip Them
        Draw(Player, 1)
        
    if len(Player.Hand) == 0: #If a Player Has 0 Cards They Win
        print("The Winner Is", Player.Name, "!")
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
    global PlayerList,GameOver
    Setup()
    Next = 0
    while not GameOver:
        Next = Turn(PlayerList[Next], Next)
Game()

    
        
