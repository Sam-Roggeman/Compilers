class Node:
    _data = None
    _type = None

    def __init__(self, _data, _type):
        self._data = _data.getText()
        self._type = _type

    def tostring(self):
        return str(self._type) + ": \"" + self._data + "\""


# todo general node
class GenNode:
    def __init__(self):
        pass

    def toString(self):
        return ""

    def getChildren(self):
        return []
    def toDot(self, dot):
        dot.node(str(id(self)), self.toString())
        for child in self.getChildren():
            child.toDot(dot)
            dot.edge(str(id(self)), str(id(child)))
        return dot

class ProgramNode(GenNode):
    children = []

    def __init__(self):
        super().__init__()

    def addchild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def fold(self):
        for index in range(len(self.children)):
            self.children[index] = TermIntNode(self.children[index].fold())

        # todo unOp PLUS MIN !


class UnOpNode(GenNode):
    rhs = None

    def getChildren(self):
        return [self.rhs]

    def __init__(self, rhs):
        super().__init__()
        self.rhs = rhs

    def fold(self):
        self.rhs = self.rhs.fold()


class UnPlusNode(UnOpNode):
    def __init__(self, rhs):
        super().__init__(rhs)

    def toString(self):
        return "+"

    def fold(self):
        super().fold()
        return self.rhs


class UnMinNode(UnOpNode):
    def __init__(self, rhs):
        super().__init__(rhs)

    def toString(self):
        return "-"

    def fold(self):
        super().fold()
        return - self.rhs


class UnNotNode(UnOpNode):
    def __init__(self, rhs):
        super().__init__(rhs)

    def toString(self):
        return "!"

    def fold(self):
        super().fold()
        return self.rhs != 0


# TODO binOp PLUS MIN MUL DIS LT EQ GT GTE LTE NEQ MOD && ||

class BinOpNode(GenNode):
    lhs = None
    rhs = None

    def getChildren(self):
        return [self.lhs, self.rhs]

    def __init__(self, lhs, rhs):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs

    def fold(self):
        self.lhs = self.lhs.fold()
        self.rhs = self.rhs.fold()


class BinPlusNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "+"

    def fold(self):
        super().fold()
        return self.lhs + self.rhs


class BinMinNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "-"

    def fold(self):
        super().fold()
        return self.lhs - self.rhs


class BinMulNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "*"

    def fold(self):
        super().fold()
        return self.lhs * self.rhs


class BinDisNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "/"

    def fold(self):
        super().fold()
        return self.lhs / self.rhs


class BinLTNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "<"

    def fold(self):
        super().fold()
        return self.lhs < self.rhs


class BinEQNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "=="

    def fold(self):
        super().fold()
        return self.lhs == self.rhs


class BinGTNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return ">"

    def fold(self):
        super().fold()
        return self.lhs > self.rhs


class BinGTENode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return ">="

    def fold(self):
        super().fold()
        return self.lhs >= self.rhs


class BinLTENode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "<="

    def fold(self):
        super().fold()
        return self.lhs <= self.rhs


class BinNENode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "!="

    def fold(self):
        super().fold()
        return self.lhs != self.rhs


class BinModNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "%"

    def fold(self):
        super().fold()
        return self.lhs % self.rhs


class BinAndNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "&&"

    def fold(self):
        super().fold()
        return self.lhs and self.rhs


class BinOrNode(BinOpNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def toString(self):
        return "||"

    def fold(self):
        super().fold()
        return self.lhs or self.rhs


class TermNode(GenNode):
    def __init__(self):
        super().__init__()


class TermIntNode(TermNode):
    value = 0

    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def toString(self):
        return str(self.value)

    def fold(self):
        return self.value

    # def __add__(self, other):
    #     self.value += other.value
    #
    # def __neg__(self):
    #     self.value = -self.value
