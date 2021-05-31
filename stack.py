class Stack:
    class Container:
        def __init__(self, content=None, next=None):
            self.content = content
            self.next = None

    def __init__(self, name=None):
        self.__top = None
        self.top = None
        self._length = 0
        self.name = name

    def is_empty(self):
        if not self.__top:
            return True
        else:
            return False

    def push(self, card):
        container = Stack.Container(card, next=self.top)
        self.__top = container
        self.top = self.__top.content
        self._length += 1

    def pop(self):
        if self.is_empty():
            return None
        content = self.__top.content
        self.__top = self.__top.next
        if self.__top == None:
            self.top = None
        else:
            self.top = self.__top.content
        self._length -= 1
        return content

    def get_length(self):
        return self._length

    # len(self) is identical to self.get_length()
    def __len__(self):
        return self._length

    # allows stack indexing: mystack[i]
    def __getitem__(self, i):
        if i >= self._length:
            raise IndexError()
        j = self._length - i - 1
        current = self.__top
        for i in range(j):
            current = current.next
        return current.content

    # allows to use stack in for statement: for card in mystack
    def __iter__(self):
        l = []
        current = self.__top
        while current != None:
            l.append(current.content)
            current = current.next
        return iter(l)
