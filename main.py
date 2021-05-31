import tkinter
from PIL import ImageTk, Image
import card as cardclass
import game
import stack

class Drawer:
    def __init__(self, game):
        # initialize tkinter window/canvas manager
        self.__game = game

        # window settings
        self.__window = tkinter.Tk("Patience")
        self.__window.title("Patience")
        self.__window.iconbitmap('./assets/spades.ico')

        # card and canvas settings
        self._card_width, self._card_height = 112.5, 175
        self._width, self._height = 25*8 + self._card_width*7, 1000
        self.__canvas = tkinter.Canvas(self.__window, width=self._width, height=self._height, bg="#008000")
        self.__window.minsize(int(self._width//1), int(self._height//1))
        self.__canvas.pack()

        # premenné pre UI ťahov
        self.__holding = None
        self.__valid_moves = []

        # začiatok potiahnutia karty
        def mouse_down(event):
            x, y = event.x, event.y

            # if click begins in the deck-waste-foundation area
            if y < 25 + self._card_height:
                # if click begins at the waste
                if 25 + 1*(25 + self._card_width) < x < 2*(25 + self._card_width):
                    self.pick_up(self.__game._waste.top)
                # if click begins at the foundations
                elif 25 + 3*(25 + self._card_width) < x < 7*(25 + self._card_width):
                    x = x - (25 + 3*(25 + self._card_width))
                    if x%(25 + self._card_width) > self._card_width:
                        return
                    i = int(x//(25 + self._card_width))
                    self.pick_up(self.__game._foundations[i].top)
            # if click begins in  the tableau area
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

        # pustenie myši
        def mouse_up(event):
            x, y = event.x, event.y

            # if click ends in the deck-waste-foundation area
            if y < 25 + self._card_height:
                # if click ends at the deck
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
                # if click ends at the foundations
                elif 25 + 3*(25 + self._card_width) < x < 7*(25 + self._card_width) and self.__holding != None:
                    if x%(25 + self._card_width) <= self._card_width:
                        i = int(x//(25 + self._card_width))
                        if self.__game._foundations[i] in self.__valid_moves and len(self.__holding) == 1:
                            self.drop(self.__game._foundations[i], "foundation")
                            return
            # if click ends in the tableau area
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
            # if cards are not placed in a suitable spot, they return to where they came from
            self.drop(self.__holding[0]._location, None)

        # canvas events
        self.__canvas.bind("<ButtonPress-1>", mouse_down)
        self.__canvas.bind("<ButtonRelease-1>", mouse_up)

    # take the card and everything on top of it
    def pick_up(self, card):
        print(type(card))
        # there should not be any cards left over in the player hand
        if self.__holding != None:
            raise Exception("This action would cause one or multiple cards to duplicate or vanish.")
        self.__holding = stack.Stack()
        current = None
        # pridávaj karty do ruky až kým nemáme vrátane tej na ktorú bolo kliknuté
        while current != card:
            current = card._location.pop()
            self.__holding.push(current)
            self.delete(current)
        self.__valid_moves = self.__game.list_valid_moves(card)
        print(self.__valid_moves)

    # place the contents of the hand at the destination
    def drop(self, destination, type=None):
        while not self.__holding.is_empty():
            current = self.__holding.pop()
            # vytvor správny objekt (objekt ukladá pozíciu karty)
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
        # vyprázdni ruku
        self.__holding = None

    # zloženie funkcií pick_up a drop
    def move(self, card, destination, type=None):
        self.pick_up(card)
        self.drop(destination, type)

    def prep_board(self):
        # pozície na ploche, kde sa nachádzajú spodky balíčkov.
        for coords in [ [81.25, 112.5], [219.25, 112.5],                  [495.25, 112.5], [633.25, 112.5], [771.25, 112.5], [909.25, 112.5],
                        [81.25, 312.5], [219.25, 312.5], [357.25, 312.5], [495.25, 312.5], [633.25, 312.5], [771.25, 312.5], [909.25, 312.5] ]:
            self.__canvas.create_image(coords[0], coords[1], anchor="center", image=emptypile)
            #if len(coords) == 3:
            #    self.__canvas.create_image(coords[0], coords[1], anchor="center", image=empties[coords[2]])

    def start(self):
        # spusti tkinter aplikáciu
        self.__window.mainloop()

    def draw(self, cards, shadow=0):
        # vyber správnu variáciu tieňu karty
        if shadow == 0:
            shadow = vshadow
        # vykresli každú passnutú kartu
        for card in cards:
            # tag je pre účel mazania kariet z plochy (pre prípad presúvania)
            tag = self.generate_tag(card)
            self.__canvas.delete(tag)
            # insert image at x, y
            x, y = card.x, card.y
            w, h = 112.5, 175
            if True and card._revealed:
                # lícom nahor
                self.__canvas.create_image(x, y, anchor="center", image=shadow, tag=tag)
                self.__canvas.create_image(x, y, anchor="center", image=images[card.get_suit()][card.get_rank()], tag=tag)
            else:
                # rubom nahor
                self.__canvas.create_image(x, y, anchor="center", image=shadow, tag=tag)
                self.__canvas.create_image(x, y, anchor="center", image=cardback, tag=tag)

    def generate_tag(self, card):
        # napríklad "s12" == queen of spades
        return "{}{}".format(card.get_suit()[0], card.get_rank())

    def delete(self, *names):
        # zmaž kartu z plochy (podľa tagu alebo karty)
        for name in names:
            if isinstance(name, cardclass.Card):
                name = self.generate_tag(name)
            self.__canvas.delete(name)

def random_cards():
    import random
    l = []
    # vygeneruj karty
    for rank in range(1, 14):
        for suit in ["hearts", "diamonds", "spades", "clubs"]:
            card = cardclass.Card(suit=suit, rank=rank, location=None, revealed=False)
            l.append(card)
    random.shuffle(l)
    start = 0
    current = 0
    # rozmiestni karty na tableau
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

    # zvyšok kariet ide do balíčku
    for j in range(i, len(l)):
        l[j] = cardclass.DeckCard(l[j], deck.get_length())
        l[j].set_location(game1._deck)
        deck.push(l[j])

    # vráť najprv TableauCards a potom DeckCards
    return l[:i], l[i:]

game1 = game.Game()
tableaus = game1._tableaus
deck = game1._deck

drawer = Drawer(game1)

# načítaj obrázky kariet
# v images sa karty nachádzajú v nasledujúcom tvare: images["spades"][12] == queen of spades
images = {}
for suit in ["clubs", "diamonds", "hearts", "spades"]:
    images[suit] = [None] # neexistuje karta ktorá má rank rovný 0
    # ak ["a"] nahradíme [1], bude vybraná druhá (grafická) varianta esa. poloha uloženého obrázka (v images) sa tým nezmení.
    for rank in ["a"] + list(range(2, 14)):
        images[suit].append(ImageTk.PhotoImage(Image.open("assets/{}{}.png".format(suit[0], rank))))
# rub karty
cardback = ImageTk.PhotoImage(Image.open("assets/cardback.png"))
# tiene (idú pod kartu aby boli vidno hranice medzi kartami)
vshadow = ImageTk.PhotoImage(Image.open("assets/vshadow.png"))
hshadow = ImageTk.PhotoImage(Image.open("assets/hshadow.png"))
# grafika prázdnych kôpok
emptypile = ImageTk.PhotoImage(Image.open("assets/empty.png"))
empties = {suit:ImageTk.PhotoImage(Image.open("assets/empty{}.png".format(suit))) for suit in "cdhs"}

# inicializácia (toto chceme neskôr presunúť do game.start() alebo niečo také)
v, h = random_cards()
drawer.prep_board()
drawer.draw(v)
drawer.draw(h, shadow=None)
#drawer.delete(*["{}{}".format("d", rank) for rank in range(1, 14)])
drawer.start()
