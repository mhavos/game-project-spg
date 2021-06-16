from stack import Stack
from drawer import Drawer
import card as cardclass

class Game:
    def __init__(self):
        # vytvorenie stackov - kopok
        self._deck = Stack()
        self._waste = Stack()
        self._foundations = []
        for _ in range(4):
            self._foundations.append(Stack())
        self._tableaus = []
        for _ in range(7):
            self._tableaus.append(Stack())

        self._drawer = Drawer(self)

    def init(self):
        # vytvori novu hru
        v, h = self.shuffle()
        self._drawer.prep_board()
        self._drawer.draw(v[:7], shadow=None)
        self._drawer.draw(v[7:])
        self._drawer.draw(h, shadow=None)

    def start(self):
        # spusti mainloop
        self._drawer.start()

    def init_drawer(self):
        # loadne hru
        self._drawer.prep_board()
        for pilegroup in [self._tableaus, self._foundations, [self._deck], [self._waste]]:
            for pile in pilegroup:
                l = list(pile)
                l.reverse()
                self._drawer.draw(l)

    def shuffle(self):
        # rozda karty
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
            l[i] = cardclass.TableauCard(l[i], current, self._tableaus[current].get_length())
            l[i].set_location(self._tableaus[current])
            self._tableaus[current].push(l[i])
            current += 1
        for pile in self._tableaus:
            pile.top.reveal()

        # zvyšok kariet ide do balíčku
        for j in range(i, len(l)):
            l[j] = cardclass.DeckCard(l[j], self._deck.get_length())
            l[j].set_location(self._deck)
            self._deck.push(l[j])

        # vráť najprv TableauCards a potom DeckCards
        return l[:i], l[i:]

    def check_win(self):
        # skontroluj, ci je hra vyhrata
        full_foundations = True
        for foundation in self._foundations:
            if foundation.get_length() < 13:
                full_foundations = False
        return full_foundations

    def move_card(self, card, stack):
        # presunut kartu do ineho stacku
        stack.push(card)
        card._location.pop()
        card.set_location(stack)

    def deck_to_waste(self):
        # prevratit kartu z deck do waste
        self._waste.push(self._deck.top)
        self._deck.pop()
        self._waste.top.reveal()


    def list_valid_moves(self, card):
        # najde a vrati vsetky miesta, kde sa da polozit karta
        valid_moves = []
        if not card:
            return valid_moves

        # najdi vhodne miesta vo foundations
        for i in range(4):
            # ak karta je A a stack je prazdny, alebo ak karta je rovnaky znak a o 1 vacsia ako top stacku
            if self._foundations[i].top == None:
                if card.get_rank() == 1:
                    valid_moves.append(self._foundations[i])
                    break
            # na foundations sa vklada vzostupne vramci znaku,
            elif self._foundations[i].top.get_suit() == card.get_suit() and self._foundations[i].top.get_rank() == card.get_rank() - 1:
                if self._foundations[i].get_length() < 13:
                    valid_moves.append(self._foundations[i])
                    break

        # najdi vhodne miesta na tableau
        for j in range(7):
            # kral moze byt vlozeny na prazdne miesto
            if self._tableaus[j].top == None:
                if card.get_rank() == 13:
                    valid_moves.append(self._tableaus[j])
            # na tableus sa vklada zostupne po striedavych farbach
            elif card.get_color_name() != self._tableaus[j].top.get_color_name() and self._tableaus[j].top.get_rank() == card.get_rank() + 1:
                # vrchny limit pre pocet kariet na tableaus
                if self._tableaus[j].get_length() < 13:
                    if self._tableaus[j].top.is_revealed():
                        valid_moves.append(self._tableaus[j])
        return valid_moves

    def get_dict(self):
        return self.__dict__