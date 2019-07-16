import random, time
c,v,topcard,ps,turnnumber,p1,p2,gameover = ["R", "G", "B", "Y"],["w", "wd", "d2", "d2", "s", "s", "r", "r", "0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9"],[],[],0,0,0,False
class card:
    def __init__(self, c, v, d):
            self.color = c #str
            self.value = v #str
            self.draws = d #int         
class player:
    def __init__(self, n, d, w):
            self.name = n #str
            self.deck = d #lst
            self.wins = w #int        
def draw():
    drawcard = card(c[random.randrange(0,3)], v[random.randrange(0,26)], 0)
    if (drawcard.value in [v[0], v[1]]):
        if (drawcard.value == v[1]):
            drawcard.draws = 4
        drawcard.color = "W"
    elif (drawcard.value in [v[2], v[3]]):
        drawcard.draws = 2
    return [drawcard.color, drawcard.value, drawcard.draws]
def skip(player, nextplayer):
    print(nextplayer.name, "got skipped!")
    playerturn(player)
def playerturn(player):
    global topcard,turnnumber,gameover,p1,p2,ps
    i = 0
    print(player.name, "'s turn!")
    if (player == p1):
        nextplayer = p2
    else:
        nextplayer = p1
    usablecards = []
    ints = []
    while i < len(player.deck):
        if (player.deck[i][0] == topcard[0] or player.deck[i][1] == topcard[1] or player.deck[i][1] in [v[0], v[1]]):
            usablecards.append(player.deck[i])
            ints.append(i)
        i = i + 1
    if (len(usablecards) > 0):
        print("Current card:", topcard)
        print("Your Cards:", usablecards)
        userinput = int(input("".join(["What card are you going to play? 1-", str(len(usablecards)), " >>>"])))
        topcard = usablecards[int(userinput - 1)]
        if (player.deck[ints[userinput - 1]][1] in [v[0], v[1]]):
            topcard[0] = input("What color? (R/G/B/Y) (Need to be exact) >>>")
            if (player.deck[ints[userinput - 1]][1] == v[1]):
                nextplayer.deck.append((draw))
                nextplayer.deck.append((draw))
                nextplayer.deck.append((draw))
                nextplayer.deck.append((draw))
        elif (player.deck[ints[userinput - 1]][1] in [v[2], v[3]]):
            nextplayer.deck.append((draw))
            nextplayer.deck.append((draw))
        elif (player.deck[ints[userinput - 1]][1] in [v[4], v[5], v[6], v[7]]):
            skip(player, nextplayer)
        player.deck.pop(ints[userinput - 1])            
    elif (len(usablecards) == 0):
        print("Sorry, you dont have any playable cards! You will have to draw and miss your turn.")
        player.deck.append(draw())
def setup():
    global topcard,turnnumber,gameover,p1,p2,ps
    c = 0
    p1 = player(input("What is player 1's name? >>>"), [], 0)
    p2 = player(input("What is player 2's name? >>>"), [], 0)
    ps = [p1,p2]
    while c <= 6:
        p1.deck.append(draw())
        p2.deck.append(draw())
        c = c + 1     
def game():
    global topcard,turnnumber,gameover,p1,p2,ps
    setup()
    topcard = draw()
    while (gameover == False):
        playerturn(ps[turnnumber])
        turnnumber = turnnumber + 1
        playerturn(ps[turnnumber])
        turnnumber = 0
game()
