class Card:
    def __init__(self, suit, rank, location, revealed):
        self._suit = suit
        self._rank = rank
        self._location = location
        self._revealed = revealed #which side faces up
        self.child = None

    def get_suit(self):
        return self._suit

    def get_rank(self):
        return self._rank

    def get_location(self):
        return self._location
    def set_location(self, location):
        self._location = location

    def get_color_name(self): # determine color based on the suit
        if self._suit in ("hearts", "diamonds"):
            return "red"
        elif self._suit in ("spades", "clubs"):
            return "black"
        else:
            return None

    def is_revealed(self):
        return self._revealed
    def reveal(self, revealed=True):
        self._revealed = revealed
    def hide(self, revealed=False):
        self._revealed = revealed

class TableauCard(Card):
    def __init__(self, card, tableau_index, tableau_depth):
        suit, rank, location, revealed = card.get_suit(), card.get_rank(), card.get_location(), card.is_revealed()
        super().__init__(suit, rank, location, revealed)
        card.child = self
        self.parent = card
        self.x = tableau_index*(25 + 112.5) + 25 + 112.5/2
        self.y = tableau_depth*40 + 2*25 + 3/2*175

class DeckCard(Card):
    def __init__(self, card, deck_depth):
        suit, rank, location, revealed = card.get_suit(), card.get_rank(), card.get_location(), card.is_revealed()
        super().__init__(suit, rank, location, revealed)
        card.child = self
        self.parent = card
        self.x = deck_depth*0 + 25 + 112.5/2
        self.y = - deck_depth*1 + 25 + 1/2*175

class WasteCard(Card):
    def __init__(self, card, waste_depth):
        suit, rank, location, revealed = card.get_suit(), card.get_rank(), card.get_location(), card.is_revealed()
        super().__init__(suit, rank, location, revealed)
        card.child = self
        self.parent = card
        self.x = waste_depth*0 + 2*25 + 3/2 * 112.5
        self.y = - waste_depth*1 + 25 + 1/2*175

class FoundationCard(Card):
    def __init__(self, card, foundation_index, foundation_depth):
        suit, rank, location, revealed = card.get_suit(), card.get_rank(), card.get_location(), card.is_revealed()
        super().__init__(suit, rank, location, revealed)
        card.child = self
        self.parent = card
        self.x = foundation_index*(25 + 112.5) + 4*25 + 7/2 * 112.5
        self.y = - foundation_depth*1 + 25 + 1/2*175

class HoldingCard(Card):
    def __init__(self, card, x, y):
        suit, rank, location, revealed = card.get_suit(), card.get_rank(), card.get_location(), card.is_revealed()
        super().__init__(suit, rank, location, revealed)
        self.parent = card
        self.x = x
        self.y = y
