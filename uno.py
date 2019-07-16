import random
colors = ["R", "B", "G", "Y", "W"] #List of colors
draws = ["0", "4", "2", "2", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"] #List of draws (same lengh as values so you do not have to split the d2 and wd up into different lists)
values = ["w", "wd", "d2", "d2", "r", "r", "s", "s", "0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9"] #List of values (probablities correct)
class card: #defines the card class
    def __init__(self, c, v, d): #gets components of the specific card you are going to make w/ the class
            self.color = c
            self.value = v
            self.draws = d
def draw(): #funtion to generate a new card
    RV = random.randrange(0,26) #RV is short for Random Value
    RC = random.randrange(0,3) #RC is short for Random Color
    RD = RV #RD is the same as RV but naming it RD looks nicer (it stands for Random Draw)
    drawncard = card(colors[RC], values[RV], draws[RD]) #declares drawncard and assigns it with the card class
    if (drawncard.value == "w" or "wd"): #if the card is wild then set the color to "W" so we can change it during play
        drawncard.color = colors[4] 
    return drawncard.color, drawncard.value, drawncard.draws #return all values of the card drawn

