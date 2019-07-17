import random
c,v,discard,p1,p2,p3,p4,gameover,reverse = ["R", "G", "B", "Y"],["w", "wd", "d2", "d2", "s", "s", "r", "r", "0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9"],[],0,0,0,0,False,False
class card:
    def __init__(self, color, value): self.color,self.value = color,value      
class player:
    def __init__(self, name, deck, next): self.name,self.deck,self.next = name,deck,next
def draw():
    global c,v
    draw = card(c[random.randrange(0,3)], v[random.randrange(0,26)])
    if (draw.value in [v[0], v[1]]):
        draw.color = "W"
    return [draw.color, draw.value]
def drawcards(player, amount):
    for _ in range(amount):
        player.deck.append(draw())
    print(player.name, "had to draw", amount, "cards!")
def playerturn(player):
    global c,v,p1,p2,p3,p4,gameover,discard,reverse
    usablecards,unusablecards,ints,i,nextplayer = [],player.deck,[],0,p2
    print("\n", player.name, "'s turn!")
    if (reverse == False):
        nextplayer = player.next[0]
    elif (reverse == True):
        nextplayer = player.next[1]
    for i in range(len(player.deck)):
        if (player.deck[i][0] == discard[0] or player.deck[i][1] == discard[1] or player.deck[i][1] in [v[0], v[1]]):
            usablecards.append(player.deck[i])
            ints.append(i)
        i =+ 1
    i = 0
    for i in range(int(len(ints) - 1)):
        unusablecards.pop(ints[i])
        i =+ 1
    if (len(usablecards) > 0):
        print("You have", len(player.deck), "cards.", "\nCurrent discard:", discard, "\nYour UnplayableCards:", unusablecards, "\nYour Playable Cards:", usablecards)
        userinput = int(input("".join(["What card are you going to play? 1-", str(len(usablecards)), " >>>"])))
        discard = usablecards[int(userinput - 1)]
        if (player.deck[ints[userinput - 1]][1] in [v[0], v[1]]):
            while (discard[0] not in ["R", "G", "B", "Y"]):
                print("\nYour Deck:", player.deck)
                discard[0] = input("What color? (R/G/B/Y) (Need to be exact) >>>")
            if (player.deck[ints[userinput - 1]][1] == v[1]):
                drawcards(nextplayer, 4)
                if (reverse == False):
                    nextplayer = nextplayer.next[0]
                elif (reverse == True):
                    nextplayer = nextplayer.next[1]
        elif (player.deck[ints[userinput - 1]][1] in [v[2], v[3]]):
            drawcards(nextplayer, 2)
        elif (player.deck[ints[userinput - 1]][1] in [v[4], v[5]]):
            if (reverse == False):
                nextplayer = nextplayer.next[0]
            elif (reverse == True):
                nextplayer = nextplayer.next[1]
        elif (player.deck[ints[userinput - 1]][1] in [v[6], v[7]]):
            reverse = not reverse
            if (reverse == False):
                nextplayer = player.next[0]
            elif (reverse == True):
                nextplayer = player.next[1]
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
        p1,p2 = player(input("What is player 1's name? >>>"), [], []),player(input("What is player 2's name? >>>"), [], [])
        p1.next,p2.next = [p2, p1],[p1, p2]
    elif (np == 3):
        p1,p2,p3 = player(input("What is player 1's name? >>>"), [], []),player(input("What is player 2's name? >>>"), [], []),player(input("What is player 3's name? >>>"), [], [])
        p1.next,p2.next,p3.next = [p2, p3],[p3, p1],[p1, p2]
    elif (np == 4):
        p1,p2,p3,p4 = player(input("What is player 1's name? >>>"), [], []),player(input("What is player 2's name? >>>"), [], []),player(input("What is player 3's name? >>>"), [], []),player(input("What is player 1's name? >>>"), [], [])
        p1.next,p2.next,p3.next,p4.next = [p2, p4],[p3, p1],[p4, p2],[p1, p3]
    for _ in range(7):
        p1.deck.append(draw())
        p2.deck.append(draw())
        if (np > 2):
            p3.deck.append(draw())
            if (np > 3):
                p4.deck.append(draw())
def game():
    global discard,p1,p2,p3,p4
    if (setup() == False):
        game()
    else:
        discard = draw()
        while (discard[1] in ["w", "wd", "d2", "d2", "s", "s", "r", "r"]):
            discard = draw()
        nxt = playerturn(p1)
        while (gameover == False):
            nxt = playerturn(nxt)
game()
