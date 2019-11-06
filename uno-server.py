from server import *
from random import sample, randrange
from operator import add, sub
Start(9274)

class Player:
    def __init__(self, Name, ConnectionObject):
        self.Name = Name
        self.Hand = []
        self.Send = ConnectionObject.Send
        self.Get = ConnectionObject.Get

class Card:
    def __init__(self, Color, Value):
        if Value not in Values[19:20]:
            self.Color = Color
        else:
            self.Color = "W"
        self.Value = Value

def Ask(ConnectionObject, Question, InputText):
    ConnectionObject.Send(f"{Question}`y`{InputText}")
    Message = ConnectionObject.Get()
    return Message

def SendToAll(Message):
    if Message:
        Message = "`GameOver` "
    i = 0
    while i < len(Players):
        Players[i].Send(f"{Message}`n` ")
        i = i + 1

def CardOut(List):
    Temp = []
    i = 0
    while i in range(len(List)):
        Temp.append(''.join([List[i].Color, List[i].Value]))
        i = i + 1
    return Temp

def Draw(Player, Number):
    global Colors, Values
    for _ in range(Number):
        Draw = Card(sample(Colors, 1)[0], sample(Values, 1)[0])
        Player.Hand.append(Draw)
    if Number not in [1, 7]:
        SendToAll(f"\n {Player.Name} had to draw {Number} cards.")
    return True

def Turn(Player):
    global Top, Players, RList, Reverse, GameOver, Colors, Values

    Skip = False
    Usable = []
    Ints = []
    i = 0
    while i in range(len(Player.Hand)):
        if Player.Hand[i].Color in [Top.Color, "W"] or Player.Hand[i].Value == Top.Value:
            Usable.append(Player.Hand[i])
            Ints.append(i)
        i = i + 1

    SendToAll(f"{Player.Name}'s turn!")

    if len(Usable) > 0:
        #OTHER INFO (SEND SOME TO ALL SEND SOME TO ONLY PLAYER)

        while True:
            try:
                In = int(Ask(Player, f"What card do you want to play? 1-{str(len(Usable))}", ">>> "))
                if In < int(len(Usable) + 1) and In > 0:
                    In = In - 1
                    break
                else:
                    raise ValueError
            except ValueError:
                Player.Send(f"Please input a valid number`n` ")
                pass

        Top = Usable[In]

        if Top.Color == "W":
            while True:
                try:
                    Color = str(Ask(Player, f"What color? (r/g/b/y)", ">>> ")).upper()
                    if "Y" in Color:
                        Top.Color = "Y"
                    elif "G" in Color:
                        Top.Color = "G"
                    elif "R" in Color:
                        Top.Color = "R"
                    elif "B" in Color:
                        Top.Color = "B"
                    else:
                        Player.Send(f"Not a valid input!`n` ")
                        pass
                    if Top.Color in Colors:
                        break
                except (ValueError, IndexError):
                    pass

        Players = Players[RList[Reverse]:] + Players[:RList[Reverse]]
        Next = Players[0]

        if Top.Value == "D":
            Draw(Next, 4)
            SendToAll(f"{Next.Name} had to draw 4 cards!")
            Skip = True
        if Top.Value == "D2":
            Draw(Next, 2)
            SendToAll(f"{Next.Name} had to draw 2 cards!")
            Skip = True
        if Top.Value == "S":
            Skip = True
        if Top.Value == "R":
            Reverse = not Reverse
            SendToAll(f"Reverse!")
            Players = Players[RList[Reverse]:] + Players[:RList[Reverse]]
            Players = Players[RList[Reverse]:] + Players[:RList[Reverse]]

        if Skip:
            SendToAll(f"{Next.Name} was skipped!")
            Players = Players[RList[Reverse]:] + Players[:RList[Reverse]]

        Player.Hand.pop(Ints[In])

    elif len(Usable) == 0:
        if len(Player.Hand) > 0:
            Player.Send(f"You have no usable cards, so you will draw.`n` ")
            Draw(Player, 1)
        elif len(Player.Hand) < 0:
            SendToAll(f"{Player.Name} won!")
            GameOver = True
            SendToAll(GameOver)

    return Players[0]

Colors = ["R", "G", "B", "Y"]
Values = ["0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9", "", "D", "D2", "D2", "S", "S", "R", "R"]

Top = Card(Colors[randrange(0, 3)], Values[randrange(0, 18)])
while Top.Value not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
    Top = Card(Colors[randrange(0, 3)], Values[randrange(0, 18)])
Players = []
RList = {False : 1, True : -1}
Reverse = False
GameOver = False

while True:
    try:
        NumberOfPlayers = int(input(f"How many Players? >>> "))
        if NumberOfPlayers < 1:
            raise ValueError
        break
    except:
        print(f"Please input a valid number.")
        pass

i = 0
while i < NumberOfPlayers:
    TempConnect = Connect()
    TempConnect
    TempPlayer = Player(Ask(TempConnect, f"What is your name?", f">>> "), TempConnect)
    Draw(TempPlayer, 7)
    Players.append(TempPlayer)
    i = i + 1

Next = Players[0]
while not GameOver:
    Next = Turn(Next)
