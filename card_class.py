class Card:
    def __init__(self, symbol, value, location, orientation):
        self.__symbol = symbol
        self.__value = value
        self.__location = location
        self.__orientation = orientation #which side faces up ? idk how to name it

    def get_symbol(self):
        return self.__symbol
    def set_symbol(self, symbol):
        self.__symbol = symbol

    def get_value(self):
        return self.__value
    def set_value(self, value):
        self.__value = value

    def get_location(self):
        return self.__location
    def set_location(self, location):
        self.__location = location

    def get_orientation(self):
        return self.__orientation
    def set_orientation(self, orientation):
        self.__orientation = orientation

class TableauCard(Card):
    def __init__(self, symbol, value, location, orientation, colour):
        super().__init__(symbol, value, location, orientation)
        self.__colour = colour

    def get_colour(self):
        return self.__colour
    def set_colour(self, colour):
        self.__colour = colour

