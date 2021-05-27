import tkinter
from PIL import ImageTk, Image
import card as cardclass

class Drawer:
    def __init__(self):
        # initialize tkinter window/canvas manager
        self.__window = tkinter.Tk("Patience")
        self.__canvas = tkinter.Canvas(self.__window, width=984, height=1000, bg="green")
        self.__canvas.pack()

    def start(self):
        self.__window.mainloop()

    def draw(self, cards):
        cards.sort()
        # for correct visual stacking
        for card in cards:
            # insert image at x, y
            # temporary rectangle drawer
            x, y = card.x, card.y
            w, h = 112, 175
            if True: #card._revealed:
                self.__canvas.create_image(x, y, anchor="center", image=images[card.get_suit()][card.get_rank()-1])
            else:
                self.__canvas.create_rectangle(x - w/2, y - h/2, x + w/2, y + h/2, fill="steel blue", outline="white")

def random_cards():
    import random
    l = []
    for rank in list(range(1, 14)):
        for suit in ["hearts", "diamonds", "spades", "clubs"]:
            card = cardclass.Card(suit=suit, rank=rank, location=None, revealed=False)
            # x = (pile + 1/2)*200
            # y = len(piles[pile])*80 + 150
            l.append(cardclass.TableauCard(card, 0, 0))
    random.shuffle(l)
    start = 0
    current = 0
    for i in range(len(l)):
        if current == 7:
            start += 1
            current = start
            if current == 7:
                break
        l[i].x = (current)*137 + 82
        l[i].y = len(piles[current])*40 + 150
        piles[current].append(l[i])
        current += 1
    for pile in piles:
        pile[-1].reveal()
    return l

piles = []
for i in range(7):
    piles.append([])

drawer = Drawer()
images = {}
for suit in ["clubs", "diamonds", "hearts", "spades"]:
    images[suit] = []
    for rank in ["a"] + list(range(1, 13)):
        images[suit].append(ImageTk.PhotoImage(Image.open("assets/{}{}.png".format(suit[0], rank))))
drawer.draw(random_cards())
drawer.start()
