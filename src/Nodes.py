import copy


class AbsNode:
    parent = None

    def replaceConst(self):
        children = self.getChildren()
        for index in range(len(children)):
            children[index] = children[index].replaceConst()
        return self

    def __init__(self, parent=None):
        self.parent = parent

    def toString(self):
        return ""

    def fold(self):
        return self

    def getChildren(self):
        return []

    def toDot(self, dot):
        dot.node(str(id(self)), self.toString())
        for child in self.getChildren():
            child.toDot(dot)
            dot.edge(str(id(self)), str(id(child)))
        return dot

    def preOrderTraversal(self, string: str, oneline=True, indent=0):
        if oneline:
            string += self.toString() + ","
            for child in self.getChildren():
                string = child.preOrderTraversal(string, oneline)
        else:
            for i in range(0, indent):
                string += '\t'
            string += self.toString()
            string += '\n'
            for child in self.getChildren():
                string = child.preOrderTraversal(string, oneline, indent + 1)

        return string


class TermNode(AbsNode):

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self

    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.value = value

    def __add__(self, other):
        b = copy.deepcopy(self)
        b.setValue(self.value + other.value)
        return b

    def __sub__(self, other):
        self.setValue(self.value - other.value)
        return self

    def __mul__(self, other):
        self.setValue(self.value * other.value)
        return self

    def __truediv__(self, other):
        self.setValue(self.value / other.value)
        return self

    def __lt__(self, other):
        return TermIntNode(self.value < other.value)

    def __mod__(self, other):
        self.setValue(self.value % other.value)
        return self

    def __gt__(self, other):
        return TermIntNode(self.value > other.value)

    def __le__(self, other):
        return TermIntNode(self.value <= other.value)

    def __ge__(self, other):
        return TermIntNode(self.value >= other.value)

    def __eq__(self, other):
        return TermIntNode(self.value == other.value)

    def __ne__(self, other):
        return TermIntNode(self.value != other.value)

    def __neg__(self):
        self.setValue(-self.value)
        return self

    def __pos__(self, other):
        return self

    def __and__(self, other):
        self.setValue(self.value & other.value)
        return self

    def __or__(self, other):
        self.setValue(self.value | other.value)
        return self

    # def __bool__(self):
    #     return self.value == 0

    def fold(self):
        return self


class TermIntNode(TermNode):

    def __init__(self, value: int, parent=None):
        super().__init__(value, parent)

    def setValue(self, _value: int):
        super().setValue(_value)

    def toString(self):
        return str(self.value)

    def __truediv__(self, other):
        self.setValue(self.value // other.value)
        return self


class TermFloatNode(TermNode):

    def __init__(self, value: int, parent=None):
        super().__init__(value, parent)

    def setValue(self, _value: float):
        super().setValue(_value)

    def toString(self):
        return str(self.value)


class TermCharNode(TermNode):

    def setValue(self, _value: str):
        if len(_value) == 1:
            super().setValue(_value)

    def __init__(self, value: str, parent=None):
        super().__init__(value, parent)

    def toString(self):
        return str(self.value)

    def fold(self):
        return self.value


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
            self.children[index] = self.children[index].fold()



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
        return self.rhs.getValue()


class UnMinNode(UnOpNode):
    def __init__(self, rhs, parent=None):
        super().__init__(rhs, parent)

    def toString(self):
        return "-"

    def fold(self):
        super().fold()
        return - self.rhs.getValue()


class UnNotNode(UnOpNode):
    def __init__(self, rhs, parent=None):
        super().__init__(rhs, parent)

    def toString(self):
        return "!"

    def fold(self):
        super().fold()
        return self.rhs != 0


class BinOpNode(AbsNode):
    lhs: TermNode
    rhs: TermNode

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
        # if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
        return self.lhs.getValue() + self.rhs.getValue()
        # else:
        #     return self


class BinMinNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "-"

    def fold(self):
        super().fold()
        return self.lhs.getValue() - self.rhs.getValue()


class BinMulNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "*"

    def fold(self):
        super().fold()
        return self.lhs.getValue() * self.rhs.getValue()


class BinDisNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "/"

    def fold(self):
        super().fold()
        return self.lhs.getValue() / self.rhs.getValue()


class BinLTNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "<"

    def fold(self):
        super().fold()
        return self.lhs.getValue() < self.rhs.getValue()


class BinEQNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "=="

    def fold(self):
        super().fold()
        return self.lhs.getValue() == self.rhs.getValue()


class BinGTNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return ">"

    def fold(self):
        super().fold()
        return self.lhs.getValue() > self.rhs.getValue()


class BinGTENode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent=None)

    def toString(self):
        return ">="

    def fold(self):
        super().fold()
        return self.lhs.getValue() >= self.rhs.getValue()


class BinLTENode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "<="

    def fold(self):
        super().fold()
        return self.lhs.getValue() <= self.rhs.getValue()


class BinNENode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "!="

    def fold(self):
        super().fold()
        return self.lhs.getValue() != self.rhs.getValue()


class BinModNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "%"

    def fold(self):
        super().fold()
        return self.lhs.getValue() % self.rhs.getValue()


class BinAndNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "&&"

    def fold(self):
        super().fold()
        return self.lhs.getValue() and self.rhs.getValue()


class BinOrNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "||"

    def fold(self):
        super().fold()
        # if isinstance(self.lhs, TermNode) and isinstance(self.rhs):
        return self.lhs.getValue() or self.rhs.getValue()
        # else:
        #     return self


class PointerNode(AbsNode):
    def __init__(self, parent=None):
        super().__init__(parent)


class VariableNode(AbsNode):
    _name: str
    _index: int
    _child: TermNode
    const: bool = False

    def replaceConst(self):
        if self.const:
            return self._child
        else:
            return self

    def makeConst(self):
        self.const = True

    def copy(self):
        return copy.deepcopy(self)

    def setIndex(self, index: int):
        self._index = index

    def setChild(self, child: TermNode):
        if not self.const:
            self._child = child
        else:
            raise TypeError("Const qualified object \"" + self.getName() + "\" cannot be changed")

    def getChildren(self):
        return [self._child]

    def fold(self):
        self._child = self._child.fold()
        return self

    def __init__(self, name: str, child, parent=None):
        super().__init__(parent)
        self._name = name
        self._child = child

    def getName(self):
        return self._name

    def toString(self):
        string = ""
        if self.const:
            string += "const "
        string += self.getType() + self.getName() + str(self._index)
        return string

    def getValue(self):
        return self._child

    def getType(self):
        return ""


class VariableIntNode(VariableNode):
    def __init__(self, name: str, child: TermIntNode = None, parent=None):
        if not child:
            child = TermIntNode(0)
        super().__init__(name, child, parent)

    def getType(self):
        return "int "


class VariableFloatNode(VariableNode):
    def __init__(self, name: str, child: TermFloatNode = None, parent=None):
        if not child:
            child = TermFloatNode(0)
        super().__init__(name, child, parent)

    def getType(self):
        return "float "


class VariableCharNode(VariableNode):
    def __init__(self, name: str, child: TermCharNode = None, parent=None):
        if not child:
            child = TermCharNode("")
        super().__init__(name, child, parent)

    def getType(self):
        return "char"


class PointerNode(VariableNode):
    point_to_type: str

    def __init__(self, name: str, child: TermNode or VariableNode, parent=None):
        super().__init__(name, child, parent)
        self.point_to_type = type(child)

    def toString(self):
        return self._name + "*"

    def deRef(self):
        return self._child

    def setChild(self, child: TermNode):
        self.pointTo(child)

    def pointTo(self, child: TermNode or VariableNode):
        if type(child) == self.point_to_type:
            self._child = child

    def getChildren(self):
        return [self._child]
