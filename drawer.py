import tkinter
from PIL import ImageTk, Image
import card as cardclass
import stack

class Drawer:
    def __init__(self, game):
        # initialize tkinter window/canvas manager
        self.__game = game

        # window settings
        self.__window = tkinter.Tk("Patience")
        self.__window.title("Patience")
        self.__window.iconbitmap('./assets/spades.ico')
        self.__window.resizable(False, False)

        # card and canvas settings
        self._card_width, self._card_height = 112.5, 175
        self._width, self._height = 25*8 + self._card_width*7, 1000
        self.__canvas = tkinter.Canvas(self.__window, width=self._width, height=self._height, bg="#008000")
        self.__window.minsize(int(self._width//1), int(self._height//1))
        self.__canvas.pack()

        # premenné pre UI ťahov
        self.__holding = None
        self.__valid_moves = []

        photos()

        def back_to_menu(saved_game):
            self.__window.destroy()
            from main import menu
            menu(saved_game)
        menu_button = tkinter.Button(self.__window, text="Back to Menu", bg="#008000", width=14,  command=lambda: back_to_menu(self.__game))
        menu_button.place(x=358, y=180, anchor="center")

        def motion(event):
            if self.__holding == None:
                return

            first = True
            shadow = None
            for card in self.__holding:
                self.delete([card])
                if first:
                    first = False
                    newcard = cardclass.HoldingCard(card, event.x, event.y + self._card_height/2 - 20)
                else:
                    newcard = cardclass.HoldingCard(card, event.x, newcard.y + 40)
                self.draw([newcard], shadow=shadow)
                shadow = 0

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
                    if i > 6:
                        return
                    self.pick_up(self.__game._foundations[i].top)
            # if click begins in  the tableau area
            elif 25 + (25 + self._card_height) < y and 25 < x:
                x = x - 25
                if x%(25 + self._card_width) > self._card_width:
                    return
                i = int(x//(25 + self._card_width))
                if i > 6:
                    return
                j = (y - 25 - (25 + self._card_height))//40
                l = self.__game._tableaus[i].get_length()
                if j < l + 3:
                    if j >= l:
                        j = l - 1
                    self.pick_up(self.__game._tableaus[i][j])
            motion(event)

        # pustenie myši
        def mouse_up(event):
            x, y = event.x, event.y

            # if click ends in the deck-waste-foundation area
            if y < 25 + self._card_height:
                # if click ends at the deck
                if 25 < x < 1*(25 + self._card_width):
                    if not self.__holding:
                        if self.__game._deck.top:
                            self.move(self.__game._deck.top, self.__game._waste, "waste")
                        else:
                            i = 0
                            for card in self.__game._waste:
                                self.pick_up(self.__game._waste.top)
                                self.drop(self.__game._deck, "deck", i)
                                i += 1
                        return
                # if click ends at the foundations
                elif 25 + 3*(25 + self._card_width) < x < 7*(25 + self._card_width) and self.__holding != None:
                    if x%(25 + self._card_width) <= self._card_width:
                        i = int((x - 25 - 3*(25 + self._card_width))//(25 + self._card_width))
                        if i > 6:
                            return
                        if self.__game._foundations[i] in self.__valid_moves and self.__holding.get_length() == 1:
                            self.drop(self.__game._foundations[i], "foundation")
                            return
            # if click ends in the tableau area
            elif 25 + (25 + self._card_height) < y and 25 < x:
                x = x - 25
                if x%(25 + self._card_width) <= self._card_width:
                    i = int(x//(25 + self._card_width))
                    if i > 6:
                        return
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
            if self.__holding:
                self.drop(self.__holding[0]._location, self.__holding[0]._type)

        # canvas events
        self.__canvas.bind("<ButtonPress-1>", mouse_down)
        self.__canvas.bind("<ButtonRelease-1>", mouse_up)

        self.__canvas.bind("<B1-Motion>", motion)

    # take the card and everything on top of it
    def pick_up(self, card):
        # there should not be any cards left over in the player hand
        if self.__holding:
            raise Exception("This action would cause one or multiple cards to duplicate or vanish.")

        if card == None:
            return
        if card.get_location() != self.__game._deck and not card.is_revealed():
            return

        self.__holding = stack.Stack()
        current = None
        # pridávaj karty do ruky až kým nemáme vrátane tej na ktorú bolo kliknuté
        while current != card:
            current = card._location.pop()
            self.__holding.push(current)
            self.delete(current)
        self.__valid_moves = self.__game.list_valid_moves(card)

        self.delete("valid_moves")
        for move in self.__valid_moves:
            if move.top:
                x, y = move.top.x, move.top.y
            elif move in self.__game._foundations:
                if self.__holding.get_length() > 1:
                    continue
                x, y = [[495.25, 112.5], [633.25, 112.5], [771.25, 112.5], [909.25, 112.5]][self.__game._foundations.index(move)]
            elif move in self.__game._tableaus:
                x, y = [[81.25, 312.5], [219.25, 312.5], [357.25, 312.5], [495.25, 312.5], [633.25, 312.5], [771.25, 312.5], [909.25, 312.5]][self.__game._tableaus.index(move)]
            else:
                x, y = 0, 0
            self.__canvas.create_image(x, y, anchor="center", image=validmove, tag="valid_moves")

    # place the contents of the hand at the destination
    def drop(self, destination, destination_type=None, j=None):
        source_type = None
        if self.__holding == None:
            return
        shadow = 0
        while not self.__holding.is_empty():
            source = self.__holding[0].get_location()
            current = self.__holding.pop()
            source_type = current._type
            # vytvor správny objekt (objekt ukladá pozíciu karty)
            if destination_type == "foundation":
                i = self.__game._foundations.index(destination)
                j = destination.get_length()
                current = cardclass.FoundationCard(current.parent, i, j)
                current.reveal()
                shadow = None
            elif destination_type == "tableau":
                i = self.__game._tableaus.index(destination)
                j = destination.get_length()
                if not j:
                    shadow = None
                current = cardclass.TableauCard(current.parent, i, j)
                current.reveal()
            elif destination_type == "waste":
                j = destination.get_length()
                current = cardclass.WasteCard(current.parent, j)
                current.reveal()
                shadow = None
            elif not destination_type:
                pass
            elif destination_type == "deck":
                current = cardclass.DeckCard(current.parent, j)
                current.hide()
                shadow = None
            current.set_location(destination)
            self.draw([current], shadow=shadow)
            destination.push(current)
            shadow = 0

        # vyprázdni ruku
        self.__holding = None
        if source.top and source_type != "deck":
            source.top.reveal()
            if source != destination and source_type != "waste":
                self.delete([source.top])
                shadow = 0
                if source.get_length() == 1:
                    shadow = None
                self.draw([source.top], shadow=shadow)

        self.delete("valid_moves")
        # vyhra
        if self.__game.check_win():
            self.__canvas.create_text(self._width/2, 600, anchor="center", font=("Courier", 50, 'bold'), text="gg you've won")


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
                self.__canvas.create_image(x, y, anchor="center", image=pileshadow, tag=tag)
                self.__canvas.create_image(x, y, anchor="center", image=shadow, tag=tag)
                self.__canvas.create_image(x, y, anchor="center", image=images[card.get_suit()][card.get_rank()], tag=tag)
            else:
                # rubom nahor
                self.__canvas.create_image(x, y, anchor="center", image=pileshadow, tag=tag)
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

def photos():
    global images, cardback, vshadow, hshadow, pileshadow, emptypile, empties, validmove
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
    pileshadow = ImageTk.PhotoImage(Image.open("assets/pileshadow.png"))
    # grafika prázdnych kôpok
    emptypile = ImageTk.PhotoImage(Image.open("assets/empty.png"))
    empties = {suit:ImageTk.PhotoImage(Image.open("assets/empty{}.png".format(suit))) for suit in "cdhs"}
    # povolené ťahy
    validmove = ImageTk.PhotoImage(Image.open("assets/valid_move.png"))
