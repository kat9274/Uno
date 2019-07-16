import random, time
c,v,topcard,p1,p2,p3,p4,gameover,reverse = ["R", "G", "B", "Y"],["w", "wd", "d2", "d2", "s", "s", "r", "r", "0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9"],[],0,0,0,0,False,False
class card:
    def __init__(self, color, value, draws):
            self.color = color #str
            self.value = value #str
            self.draws = draws #int         
class player:
    def __init__(self, name, deck, NextList):
            self.name = name #str
            self.deck = deck #lst
            self.nextList = NextList #list
def draw():
    global c,v
    drawcard = card(c[random.randrange(0,3)], v[random.randrange(0,26)], 0)
    if (drawcard.value in [v[0], v[1]]):
        if (drawcard.value == v[1]):
            drawcard.draws = 4
        drawcard.color = "W"
    elif (drawcard.value in [v[2], v[3]]):
        drawcard.draws = 2
    return [drawcard.color, drawcard.value, drawcard.draws]
def drawcards(nxtplayer, amount):
    for _ in range(amount):
        nxtplayer.deck.append(draw())
    print(nxtplayer.name, "had to draw", amount, "cards!")
def playerturn(player):
    global c,v,p1,p2,p3,p4,gameover,topcard,reverse
    print(player.name, "'s turn!")
    usablecards,ints,i,nextplayer = [],[],0,p2
    if (reverse == False):
        nextplayer = player.nextList[0]
    elif (reverse == True):
        nextplayer = player.nextList[1]
    for i in range(len(player.deck)):
        if (player.deck[i][0] == topcard[0] or player.deck[i][1] == topcard[1] or player.deck[i][1] in [v[0], v[1]]):
            usablecards.append(player.deck[i])
            ints.append(i)
        i =+ 1
    i = 0
    if (len(usablecards) > 0):
        print("Current card:", topcard)
        print("Your Playable Cards:", usablecards)
        userinput = int(input("".join(["What card are you going to play? 1-", str(len(usablecards)), " >>>"])))
        topcard = usablecards[int(userinput - 1)]
        if (player.deck[ints[userinput - 1]][1] in [v[0], v[1]]):
            while (topcard[0] not in ["R", "G", "B", "Y"]):
                print("Your Deck:", player.deck)
                topcard[0] = input("What color? (R/G/B/Y) (Need to be exact) >>>")
            if (player.deck[ints[userinput - 1]][1] == v[1]):
                drawcards(nextplayer, 4)
                if (reverse == False):
                    nextplayer = nextplayer.nextList[0]
                elif (reverse == True):
                    nextplayer = nextplayer.nextList[1]
        elif (player.deck[ints[userinput - 1]][1] in [v[2], v[3]]):
            drawcards(nextplayer, 2)
        elif (player.deck[ints[userinput - 1]][1] in [v[4], v[5]]):
            if (reverse == False):
                nextplayer = nextplayer.nextList[0]
            elif (reverse == True):
                nextplayer = nextplayer.nextList[1]
        elif (player.deck[ints[userinput - 1]][1] in [v[6], v[7]]):
            reverse = not reverse
            if (reverse == False):
                nextplayer = player.nextList[0]
            elif (reverse == True):
                nextplayer = player.nextList[1]
        player.deck.pop(ints[userinput - 1])            
    elif (len(usablecards) == 0):
        print("Sorry, you dont have any playable cards! You will have to draw and miss your turn.")
        player.deck.append(draw())
    if (len(player.deck) == 0):
        gameover = True
        print("The winner is", player.name, "!")
    return nextplayer
def setup():
    global p1,p2,p3,p4
    np,i = int(input("How Many Players? 2-4 >>>")),0
    if (np not in [2, 3, 4]):
        print("Not in range.")
        return False
    elif (np == 2):
        p1 = player(input("What is player 1's name? >>>"), [], [])
        p2 = player(input("What is player 2's name? >>>"), [], [])
        p1.nextList,p2.nextList = [p2, p1],[p1, p2]
    elif (np == 3):
        p1 = player(input("What is player 1's name? >>>"), [], [])
        p2 = player(input("What is player 2's name? >>>"), [], [])
        p3 = player(input("What is player 3's name? >>>"), [], [])
        p1.nextList,p2.nextList,p3.nextList = [p2, p3],[p3, p1],[p1, p2]
    elif (np == 4):
        p1 = player(input("What is player 1's name? >>>"), [], p2, p4)
        p2 = player(input("What is player 2's name? >>>"), [], p3, p1)
        p3 = player(input("What is player 3's name? >>>"), [], p4, p2)
        p4 = player(input("What is player 1's name? >>>"), [], p1, p3)
        p1.nextList,p2.nextList,p3.nextList,p4.nextList = [p2, p4],[p3, p1],[p4, p2],[p1, p3]
    for _ in range(7):
        p1.deck.append(draw())
        p2.deck.append(draw())
        if (np > 2):
            p3.deck.append(draw())
            if (np > 3):
                p4.deck.append(draw())
def game():
    global topcard,p1,p2,p3,p4
    if (setup() == False):
        game()
    else:
        topcard = draw()
        while (topcard[1] in ["w", "wd", "d2", "d2", "s", "s", "r", "r"]):
            topcard = draw()
        nxt = playerturn(p1)
        while (gameover == False):
            nxt = playerturn(nxt)
game()
