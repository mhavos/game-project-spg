from stack import Stack

class Game:
    def __init__(self):
        # create the piles as stacks
        self._deck = Stack()
        self._waste = Stack()
        self._foundations = []
        for _ in range(4):
            self._foundations.append(Stack())
        self._tableaus = []
        for _ in range(7):
            self._tableaus.append(Stack())

    def move_card(self, card, stack):
        stack.push(card)
        card._location.pop()
        card.set_location(stack)

    def deck_to_waste(self):
        # turn a card over from deck to waste
        self._waste.push(self._deck.top)
        self._deck.pop()
        self._waste.top.reveal()

    def reset_deck(self):
        # remove all cards from the waste pile and put them back inside the deck
        for i in range(self._deck.get_length()):
            self._deck.push(self._waste.top)
            self._deck.top.hide()
            self._waste.pop()

    def list_valid_moves(self, card):
        valid_moves = []
        # check available foundation spots
        for i in range(4):
            # if your card is an ace - there is a guaranteed empty spot, or if your card matches in suit and is 1 larger
            if card.get_rank() == 1 or (self._foundations[i].top.get_suit() == card.get_suit() and self._foundations[i].top.get_rank() == card.get_rank() + 1):
                if self._foundations[i].get_length() < 13:
                    if self._foundations[i] != card._location:
                        valid_moves.append(self._foundations[i])
                        break

        # check available tableau spots
        for j in range(7):
            if (card.get_rank() == 13 and not self._tableaus[j].top) or (card.get_color_name() != self._tableaus[j].top.get_color_name() and self._tableaus[j].top.get_rank == card.get_rank() - 1):
                if self._tableaus[j].get_length() < 13:
                    if self._tableaus[j] != card._location:
                        valid_moves.append(self._tableaus[j])
                        break
        return valid_moves
