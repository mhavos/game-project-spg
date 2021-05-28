import tkinter
from PIL import ImageTk, Image
import card as cardclass
import game
import stack

class Drawer:
    def __init__(self, game):
        # initialize tkinter window/canvas manager
        self.__game = game

        self.__window = tkinter.Tk("Patience")
        self.__window.title("Patience")
        self.__window.iconbitmap('./assets/spades.ico')

        self._card_width, self._card_height = 112.5, 175
        self._width, self._height = 25*8 + self._card_width*7, 1000
        self.__canvas = tkinter.Canvas(self.__window, width=self._width, height=self._height, bg="#008000")
        self.__window.minsize(int(self._width//1), int(self._height//1))
        self.__canvas.pack()

        self.__holding = None
        self.__valid_moves = []

        def mouse_down(event):
            x, y = event.x, event.y
            if y < 25 + self._card_height:
                if 25 + 1*(25 + self._card_width) < x < 2*(25 + self._card_width):
                    self.pick_up(self.__game._waste.top)
                elif 25 + 3*(25 + self._card_width) < x < 7*(25 + self._card_width):
                    x = x - (25 + 3*(25 + self._card_width))
                    if x%(25 + self._card_width) > self._card_width:
                        return
                    i = int(x//(25 + self._card_width))
                    self.pick_up(self.__game._foundations[i].top)
            elif 25 + (25 + self._card_height) < y and 25 < x:
                x = x - 25
                if x%(25 + self._card_width) > self._card_width:
                    return
                i = int(x//(25 + self._card_width))
                j = (y - 25 - (25 + self._card_height))//40
                l = self.__game._tableaus[i].get_length()
                if j < l + 3:
                    if j >= l:
                        j = l - 1
                    self.pick_up(self.__game._tableaus[i][j])

        def mouse_up(event):
            x, y = event.x, event.y
            if y < 25 + self._card_height:
                if 25 < x < 1*(25 + self._card_width):
                    if self.__holding == None:
                        if self.__game._deck.top != None:
                            self.move(self.__game._deck.top, self.__game._waste, "waste")
                        else:
                            i = 0
                            for card in self.__game._waste:
                                self.__holding = card
                                self.drop(self.__game._deck, "deck{}".format(i))
                                i += 1
                            self.__game.reset_deck()
                        return
                elif 25 + 3*(25 + self._card_width) < x < 7*(25 + self._card_width) and self.__holding != None:
                    if x%(25 + self._card_width) <= self._card_width:
                        i = int(x//(25 + self._card_width))
                        if self.__game._foundations[i] in self.__valid_moves and len(self.__holding) == 1:
                            self.drop(self.__game._foundations[i], "foundation")
                            return
            elif 25 + (25 + self._card_height) < y and 25 < x:
                x = x - 25
                if x%(25 + self._card_width) <= self._card_width:
                    i = int(x//(25 + self._card_width))
                    if self.__holding != None:
                        if self.__game._tableaus[i] in self.__valid_moves:
                            self.drop(self.__game._tableaus[i], "tableau")
                            return
                    else:
                        j = (y - 25 - (25 + self._card_height))//40
                        l = self.__game._tableaus[i].get_length()
                        if l - 1 <= j < l + 3:
                            self.__valid_moves = self.__game.list_valid_moves(self.__game._tableaus[i].top)
                            for k in range(4):
                                if self.__game._foundations[k] in self.__valid_moves:
                                    self.move(self.__game._tableaus[i].top, self.__game._foundations[k], "foundation")
            self.drop(self.__holding[0]._location, None)

        self.__canvas.bind("<ButtonPress-1>", mouse_down)
        self.__canvas.bind("<ButtonRelease-1>", mouse_up)

    def pick_up(self, card):
        print(type(card))
        if self.__holding != None:
            raise Exception("This action would cause one or multiple cards to duplicate or vanish.")
        self.__holding = stack.Stack()
        current = None
        while current != card:
            current = card._location.pop()
            self.__holding.push(current)
            self.delete(current)
        self.__valid_moves = self.__game.list_valid_moves(card)
        print(self.__valid_moves)

    def drop(self, destination, type=None):
        while not self.__holding.is_empty():
            current = self.__holding.pop()
            if type == "foundation":
                i = self.__game._foundations.index(destination)
                j = len(destination)
                current = cardclass.FoundationCard(current.parent, i, j)
            elif type == "tableau":
                i = self.__game._tableaus.index(destination)
                j = len(destination)
                current = cardclass.TableauCard(current.parent, i, j)
            elif type == "waste":
                j = len(destination)
                current = cardclass.WasteCard(current.parent, j)
                current.reveal()
            elif type == None:
                pass
            elif type[:5] == "deck":
                j = int(type[5:])
                current = cardclass.DeckCard(current.parent, j)
                current.hide()
            self.draw([current])
            destination.push(self.__holding)
        self.__holding = None

    def move(self, card, destination, type=None):
        self.pick_up(card)
        self.drop(destination, type)

    def prep_board(self):
        for coords in [ [81.25, 112.5], [219.25, 112.5], [495.25, 112.5, "h"], [633.25, 112.5, "s"], [771.25, 112.5, "d"], [909.25, 112.5, "c"],
                        [81.25, 312.5], [219.25, 312.5], [357.25, 312.5], [495.25, 312.5], [633.25, 312.5], [771.25, 312.5], [909.25, 312.5] ]:
            self.__canvas.create_image(coords[0], coords[1], anchor="center", image=emptypile)
            if len(coords) == 3:
                self.__canvas.create_image(coords[0], coords[1], anchor="center", image=empties[coords[2]])

    def start(self):
        self.__window.mainloop()

    def draw(self, cards, shadow=0):
        if shadow == 0:
            shadow = vshadow
        for card in cards:
            tag = self.generate_tag(card)
            self.__canvas.delete(tag)
            # insert image at x, y
            # temporary rectangle drawer
            x, y = card.x, card.y
            w, h = 112.5, 175
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
            l.append(card)
    random.shuffle(l)
    start = 0
    current = 0
    for i in range(len(l)):
        if current == 7:
            start += 1
            current = start
            if current == 7:
                break
        l[i] = cardclass.TableauCard(l[i], current, tableaus[current].get_length())
        l[i].set_location(game1._tableaus[current])
        tableaus[current].push(l[i])
        current += 1
    for pile in tableaus:
        pile.top.reveal()
    for j in range(i, len(l)):
        l[j] = cardclass.DeckCard(l[j], deck.get_length())
        l[j].set_location(game1._deck)
        deck.push(l[j])
    return l[:i], l[i:]

game1 = game.Game()
tableaus = game1._tableaus
deck = game1._deck

drawer = Drawer(game1)

images = {}
for suit in ["clubs", "diamonds", "hearts", "spades"]:
    images[suit] = []
    for rank in ["a"] + list(range(2, 14)):
        images[suit].append(ImageTk.PhotoImage(Image.open("assets/{}{}.png".format(suit[0], rank))))
cardback = ImageTk.PhotoImage(Image.open("assets/cardback.png"))
vshadow = ImageTk.PhotoImage(Image.open("assets/vshadow.png"))
hshadow = ImageTk.PhotoImage(Image.open("assets/hshadow.png"))
emptypile = ImageTk.PhotoImage(Image.open("assets/empty.png"))
empties = {suit:ImageTk.PhotoImage(Image.open("assets/empty{}.png".format(suit))) for suit in "cdhs"}

v, h = random_cards()
drawer.prep_board()
drawer.draw(v)
drawer.draw(h, shadow=None)
#drawer.delete(*["{}{}".format("d", rank) for rank in range(1, 14)])
drawer.start()
