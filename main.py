import tkinter
from PIL import ImageTk, Image
import card as cardclass

class Drawer:
    def __init__(self):
        # initialize tkinter window/canvas manager
        self.__window = tkinter.Tk("Patience")
        self.__canvas = tkinter.Canvas(self.__window, width=984, height=1000, bg="#319331")
        self.__canvas.pack()

    def prep_board(self):
        for coords in [[81.25, 0], [219.25, 0], [357.25, 0], [495.25, 0], [633.25, 0], [771.25, 0], [909.25, 0]]:
            self.__canvas.create_image(coords[0], 25 + 1/2*175, anchor="center", image=emptypile)

    def start(self):
        self.__window.mainloop()

    def draw(self, cards, shadow=None):
        if shadow == None:
            shadow = vshadow
        cards.sort()
        # for correct visual stacking
        for card in cards:
            tag = self.generate_tag(card)
            self.__canvas.delete(tag)
            # insert image at x, y
            # temporary rectangle drawer
            x, y = card.x, card.y
            w, h = 112, 175
            if True and card._revealed:
                self.__canvas.create_image(x, y, anchor="center", image=shadow, tag=tag)
                self.__canvas.create_image(x, y, anchor="center", image=images[card.get_suit()][card.get_rank()-1], tag=tag)
            else:
                self.__canvas.create_image(x, y, anchor="center", image=shadow, tag=tag)
                self.__canvas.create_image(x, y, anchor="center", image=cardback, tag=tag)

    def generate_tag(self, card):
        return "{}{}".format(card.get_suit()[0], card.get_rank())

    def delete(self, *names):
        for name in names:
            if isinstance(name, cardclass.Card):
                name = self.generate_tag(name)
            self.__canvas.delete(name)

def random_cards():
    import random
    l = []
    for rank in range(1, 14):
        for suit in ["hearts", "diamonds", "spades", "clubs"]:
            card = cardclass.Card(suit=suit, rank=rank, location=None, revealed=False)
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
        l[i].x = (current)*138 + 25 + 112.5/2
        l[i].y = len(piles[current])*40 + 2*25 + 3/2*175
        piles[current].append(l[i])
        current += 1
    for pile in piles:
        pile[-1].reveal()
    a = i
    for i in range(i, len(l)):
        l[i].x = len(deck)*12 + 25 + 112.5/2
        l[i].y = 25 + 1/2*175
        deck.append(l[i])
    deck[-1].reveal()
    return l[:a], l[a:]

piles = []
for i in range(7):
    piles.append([])
deck = []

drawer = Drawer()

images = {}
for suit in ["clubs", "diamonds", "hearts", "spades"]:
    images[suit] = []
    for rank in ["a"] + list(range(2, 14)):
        images[suit].append(ImageTk.PhotoImage(Image.open("assets/{}{}.png".format(suit[0], rank))))
cardback = ImageTk.PhotoImage(Image.open("assets/cardback.png"))
vshadow = ImageTk.PhotoImage(Image.open("assets/vshadow.png"))
hshadow = ImageTk.PhotoImage(Image.open("assets/hshadow.png"))
emptypile = ImageTk.PhotoImage(Image.open("assets/empty.png"))

v, h = random_cards()
drawer.prep_board()
drawer.draw(v)
drawer.draw(h, shadow=hshadow)
#drawer.delete(*["{}{}".format("d", rank) for rank in range(1, 14)])
drawer.start()
