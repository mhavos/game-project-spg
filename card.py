class Card:
    def __init__(self, symbol, value, location, orientation):
        self._symbol = symbol
        self._value = value
        self._location = location
        self._orientation = orientation #which side faces up ? idk how to name it

    def get_symbol(self):
        return self._symbol
    def set_symbol(self, symbol):
        self._symbol = symbol

    def get_value(self):
        return self._value
    def set_value(self, value):
        self._value = value

    def get_location(self):
        return self._location
    def set_location(self, location):
        self._location = location

    def get_orientation(self):
        return self._orientation
    def set_orientation(self, orientation):
        self._orientation = orientation

class TableauCard(Card):
    def __init__(self, symbol, value, location, orientation, colour):
        super().__init__(symbol, value, location, orientation)
        self._colour = colour

    def get_colour(self):
        return self._colour
    def set_colour(self, colour):
        self._colour = colour
