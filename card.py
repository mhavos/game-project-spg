class Card:
    def __init__(self, suit, rank, location, revealed):
        self._suit = suit
        self._rank = rank
        self._location = location
        self._revealed = revealed #which side faces up ? idk how to name it
        self.child = None

    def get_suit(self):
        return self._symbol
    def set_suit(self, symbol):
        self._symbol = symbol

    def get_rank(self):
        return self._rank
    def set_rank(self, rank):
        self._rank = rank

    def get_location(self):
        return self._location
    def set_location(self, location):
        self._location = location

    def is_revealed(self):
        return self._revealed
    def reveal(self, revealed=True):
        self._revealed = revealed
    def hide(self, revealed=False):
        self._revealed = revealed

class TableauCard(Card):
    def __init__(self, card, x, y):
        suit, rank, location, revealed = card.get_suit(), card.get_rank(), card.get_location(), card.is_revealed()
        super().__init__(suit, rank, location, revealed)
        card.child = self
        self.x = x
        self.y = y

    def get_color_name(self):
        if self._suit in ("hearts", "diamonds"):
            return "red"
        elif self._suit in ("spades", "clubs"):
            return "black"
        else:
            return None

    def get_suit(self): # idk why i put this here
        symbols = {"hearts":"♥", "diamonds":"♦", "spades":"♠", "clubs":"♣"}
        return symbols[self._suit]

    def __lt__(self, other): # this is so that the drawer can sort the cards (so that they stack properly)
        return self._y < other._y
