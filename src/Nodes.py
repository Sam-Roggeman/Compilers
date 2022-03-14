# class Node:
#     _data = None
#     _type = None
#
#     def __init__(self, _data, _type):
#         self._data = _data.getText()
#         self._type = _type
#
#     def tostring(self):
#         return str(self._type) + ": \"" + self._data + "\""


class AbsNode:
    parent = None

    def __init__(self, parent=None):
        self.parent = parent

    def toString(self):
        return ""

    def getChildren(self):
        return []

    def fold(self):
        pass

    def toDot(self, dot):
        dot.node(str(id(self)), self.toString())
        for child in self.getChildren():
            child.toDot(dot)
            dot.edge(str(id(self)), str(id(child)))
        return dot


class ProgramNode(AbsNode):
    children = []

    def __init__(self, parent=None):
        super().__init__(parent)

    def addchild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def toString(self):
        return "Program"

    def fold(self):
        for index in range(len(self.children)):
            self.children[index] = TermIntNode(self.children[index].fold())


class UnOpNode(AbsNode):
    rhs = None

    def getChildren(self):
        return [self.rhs]

    def __init__(self, rhs, parent=None):
        super().__init__(parent)
        self.rhs = rhs

    def fold(self):
        self.rhs = self.rhs.fold()


class UnPlusNode(UnOpNode):
    def __init__(self, rhs, parent=None):
        super().__init__(rhs, parent)

    def toString(self):
        return "+"

    def fold(self):
        super().fold()
        return self.rhs


class UnMinNode(UnOpNode):
    def __init__(self, rhs, parent=None):
        super().__init__(rhs, parent)

    def toString(self):
        return "-"

    def fold(self):
        super().fold()
        return - self.rhs


class UnNotNode(UnOpNode):
    def __init__(self, rhs, parent=None):
        super().__init__(rhs, parent)

    def toString(self):
        return "!"

    def fold(self):
        super().fold()
        return self.rhs != 0


class BinOpNode(AbsNode):
    lhs = None
    rhs = None

    def getChildren(self):
        return [self.lhs, self.rhs]

    def __init__(self, lhs, rhs, parent=None):
        super().__init__(parent)
        self.lhs = lhs
        self.rhs = rhs

    def fold(self):
        self.lhs = self.lhs.fold()
        self.rhs = self.rhs.fold()


class BinPlusNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "+"

    def fold(self):
        super().fold()
        return self.lhs + self.rhs


class BinMinNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "-"

    def fold(self):
        super().fold()
        return self.lhs - self.rhs


class BinMulNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "*"

    def fold(self):
        super().fold()
        return self.lhs * self.rhs


class BinDisNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "/"

    def fold(self):
        super().fold()
        return self.lhs / self.rhs


class BinLTNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "<"

    def fold(self):
        super().fold()
        return self.lhs < self.rhs


class BinEQNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "=="

    def fold(self):
        super().fold()
        return self.lhs == self.rhs


class BinGTNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return ">"

    def fold(self):
        super().fold()
        return self.lhs > self.rhs


class BinGTENode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent=None)

    def toString(self):
        return ">="

    def fold(self):
        super().fold()
        return self.lhs >= self.rhs


class BinLTENode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "<="

    def fold(self):
        super().fold()
        return self.lhs <= self.rhs


class BinNENode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "!="

    def fold(self):
        super().fold()
        return self.lhs != self.rhs


class BinModNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "%"

    def fold(self):
        super().fold()
        return self.lhs % self.rhs


class BinAndNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "&&"

    def fold(self):
        super().fold()
        return self.lhs and self.rhs


class BinOrNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "||"

    def fold(self):
        super().fold()
        return self.lhs or self.rhs


class TermNode(AbsNode):
    def __init__(self, parent=None):
        super().__init__(parent)


class TermIntNode(TermNode):
    value: int

    def __init__(self, value: int, parent=None):
        super().__init__(parent)
        self.value = value
    def setValue(self, _value:int):
        self.value = _value
    def toString(self):
        return str(self.value)

    def fold(self):
        return self.value


class TermFloatNode(TermNode):
    value: float

    def __init__(self, value: int, parent=None):
        super().__init__(parent)
        self.value = value

    def setValue(self, value: float):
        self.value = value
    def toString(self):
        return str(self.value)

    def fold(self):
        return self.value


class TermCharNode(TermNode):
    value: str
    def setValue(self, _value:str):
        if len(_value) == 1:
            self.value = _value
    def __init__(self, value: int, parent=None):
        super().__init__(parent)
        self.value = value

    def toString(self):
        return str(self.value)

    def fold(self):
        return self.value


class PointerNode(AbsNode):
    def __init__(self, parent=None):
        super().__init__(parent)


class VariableNode(AbsNode):
    _name: str
    _child: TermNode


    def __init__(self, name: str, child, parent=None):
        super().__init__(parent)
        self._name = name
        self._child = child
    def getName(self):
        return self._name
    def toString(self):
        return self.getName() + ": " + self._child.toString()
    def setValue(self, value):
        self._child.setValue(value)

class VariableIntNode(VariableNode):
    def __init__(self, name: str, child: TermIntNode = TermIntNode(0), parent=None):
        super().__init__(name, child, parent)

    def toString(self):
        return "int " + super().toString()


class VariableFloatNode(VariableNode):
    def __init__(self, name: str, child: TermFloatNode = TermFloatNode(0), parent=None):
        super().__init__(name, child, parent)

    def toString(self):
        return "float " + super().toString()


class VariableCharNode(VariableNode):
    def __init__(self, name: str, child: TermCharNode = TermCharNode(0), parent=None):
        super().__init__(name, child, parent)

    def toString(self):
        return "char " + super().toString()





class PointerNode(VariableNode):
    point_to_type: str

    def __init__(self, name: str, child: TermNode or VariableNode, parent=None):
        super().__init__(name, child, parent)
        self.point_to_type = type(child)
    def toString(self):
        return self._name + "*"

    def pointTo(self, child: TermNode or VariableNode):
        if type(child) == self.point_to_type:
            self._child = child
    def getChildren(self):
        return [self._child]