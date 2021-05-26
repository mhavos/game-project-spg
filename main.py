import tkinter

class Drawer:
    def __init__(self):
        # initialize tkinter window/canvas manager
        self.__window = tkinter.Tk("Klondike")
        self.__canvas = tkinter.Canvas(self.__window, width=500, height=400, bg="green")
        self.__canvas.pack()

    def start(self):
        self.__window.mainloop()

    def draw(self, cards):
        cards.sort()
        # for correct visual stacking
        for card in cards:
            # insert image at x, y
            # temporary rectangle drawer
            x, y = card._x, card._y
            w, h = 45, 70
            if card._revealed:
                self.__canvas.create_rectangle(x - w/2, y - h/2, x + w/2, y + h/2, fill=card.get_color_name(), outline="white")
                self.__canvas.create_text(x, y - h/3, text="{1}{0}".format(card.get_value(), card.get_suit()), fill="white")
            else:
                self.__canvas.create_rectangle(x - w/2, y - h/2, x + w/2, y + h/2, fill="steel blue", outline="white")

class Card:
    # toto je tu len kvoli testovaniu kodu, skutocne to chce asi vyzerat inak
    def __init__(self, value, suit, revealed=True):
        self.__value = value
        self.__suit = suit
        self._revealed = revealed

        import random
        pile = random.randint(0, 6)
        self._x = 100 + pile*50
        self._y = len(piles[pile])*20 + 70
        piles[pile].append(self)

    def get_value(self):
        return self.__value

    def get_color_name(self):
        if self.__suit in ("hearts", "diamonds"):
            return "red"
        elif self.__suit in ("spades", "clubs"):
            return "black"
        else:
            return None

    def get_suit(self):
        symbols = {"hearts":"♥", "diamonds":"♦", "spades":"♠", "clubs":"♣"}
        return symbols[self.__suit]

    def __lt__(self, other):
        return self._y < other._y

def random_cards():
    import random
    l = []
    for value in ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]:
        for suit in ["hearts", "diamonds", "spades", "clubs"]:
            l.append(Card(value, suit, revealed=random.choice([True, False])))
    return l

piles = []
for i in range(7):
    piles.append([])

drawer = Drawer()
drawer.draw(random_cards())
