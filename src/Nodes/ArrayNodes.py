from Nodes.AbsNode import AbsNode


class ArrayNode(AbsNode):
    def __init__(self):
        super().__init__()
        self.next = None
        self.value = None
        self.type = None

    def setNext(self, next):
        self.next = next

    def setValue(self, value):
        self.value = value

    def setType(self, type):
        self.type = type

    def setParent(self, parent):
        self.parent = parent

    def getNext(self):
        return self.next

    def getChildren(self):
        if self.next:
            return [self.next]
        else:
            return []


class StringNode(ArrayNode):

    def __init__(self):
        super().__init__()
        self.type = 'char'

    def toString(self):
        return self.value

    def getFullString(self):
        returnval = self.value
        if self.next:
            returnval += self.next.getFullString()
        return returnval
