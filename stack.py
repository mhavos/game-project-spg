class Stack:
    def __init__(self):
        self.top = None
        self._length = 0

    def is_empty(self):
        if not self.top:
            return True
        else:
            return False

    def push(self, card):
        card.next = self.top
        self.top = card
        self._length += 1

    def pop(self):
        if self.is_empty():
            return None
        self.top = self.top.next
        self._length -= 1

    def get_length(self):
        return self._length


