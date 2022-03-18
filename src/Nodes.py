import copy
import sys


from Errors import *


class AbsNode:
    parent = None
    _metadata: MetaData
    _lvalue = True

    def getLeftMostChild(self):
        children = self.getChildren()
        if len(children):
            return children[0].getLeftMostChild()
        else:
            return self
    def getLine(self):
        return self._metadata.getLine()

    def getColumn(self):
        return self._metadata.getColumn()

    def addMetaData(self, metadata: MetaData):
        self._metadata = metadata

    def getMetaData(self):
        return self._metadata

    def setChild(self, child, index: int = 0):
        pass

    def replaceConst(self):
        children = self.getChildren()
        for index in range(len(children)):
            self.setChild(self.getChildren()[index].replaceConst(), index)
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

    def isLvalue(self):
        return self._lvalue


class TermNode(AbsNode):
    _lvalue = False
    value = None

    def __str__(self):
        return str(self.value)

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self

    def convertNode(self, child):
        return child

    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.value = value

    def __add__(self, other):
        b = copy.deepcopy(self)
        other = self.convertNode(other)
        b.setValue(self.value + other.value)
        return b

    def __sub__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value - other.value)
        return self

    def __mul__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value * other.value)
        return self

    def __truediv__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value / other.value)

        return self

    def __lt__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value < other.value)

    def __mod__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value % other.value)
        return self

    def __gt__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value > other.value)

    def __le__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value <= other.value)

    def __ge__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value >= other.value)

    def __eq__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value == other.value)

    def __ne__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value != other.value)

    def __neg__(self):
        self.setValue(-self.value)
        return self

    def __pos__(self, other):
        other = self.convertNode(other)
        return self

    def __and__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value & other.value)
        return self

    def __or__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value | other.value)
        return self

    # def __bool__(self):
    #     return self.value == 0

    def fold(self):
        return self


class TermIntNode(TermNode):
    def __truediv__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value // other.value)
        return self

    def __init__(self, value: int=None, parent=None):
        super().__init__(value, parent)

    def setValue(self, _value: int):
        _value = int(_value)
        super().setValue(_value)

    def toString(self):
        return str(self.value)

    def convertNode(self, child: TermNode):
        if isinstance(child, TermIntNode):
            return child
        elif isinstance(child, TermFloatNode):
            # warning
            sys.stderr.write("Warning: Implicit conversion from float to int, possible loss of information" + "\n")
            nchild = TermIntNode(int(child.value))
            nchild.addMetaData(child.getMetaData())
            return nchild
        elif isinstance(child, TermCharNode):
            nchild = TermIntNode(ord(child.value))
            nchild.addMetaData(child.getMetaData())
            return nchild
        elif len(child.getChildren()) != 0:
            child.setChild(self.convertNode(child.getChildren()[0]), 0)
        return child

class TermFloatNode(TermNode):

    def __init__(self, value: float= None, parent=None):
        super().__init__(value, parent)

    def setValue(self, _value: float):
        _value = float(_value)

        super().setValue(_value)

    def toString(self):
        return str(self.value)

    def convertNode(self, child: TermNode):
        if isinstance(child, TermFloatNode):
            return child
        elif isinstance(child, TermIntNode):
            nchild = TermFloatNode(float(child.value))
            nchild.addMetaData(child.getMetaData())
            return nchild

        elif isinstance(child, TermCharNode):
            nchild = TermFloatNode(float(ord(child.value)))
            nchild.addMetaData(child.getMetaData())
            return nchild
        elif len(child.getChildren()) != 0:
            child.setChild(self.convertNode(child.getChildren()[0]),0)
        return child


class TermCharNode(TermNode):

    def setValue(self, _value: str):
        _value = str(_value)

        if len(_value) == 1:
            super().setValue(_value)

    def __init__(self, value: str = None, parent=None):
        super().__init__(value, parent)

    def toString(self):
        return str(self.value)

    def fold(self):
        return self

    def convertNode(self, child: TermNode):
        if isinstance(child, TermCharNode):
            return child
        elif isinstance(child, TermFloatNode):
            sys.stderr.write("Warning: Implicit conversion from float to char, possible loss of information " + "\n")
            nchild = TermCharNode(chr(int(child.value)))
            nchild.addMetaData(child.getMetaData())
            return nchild
        elif isinstance(child, TermIntNode):
            sys.stderr.write("Warning: Implicit conversion from int to char, possible loss of information " +  "\n")
            nchild = TermCharNode(chr(child.value))
            nchild.addMetaData(child.getMetaData())
            return nchild
        elif len(child.getChildren()) != 0:
            child.setChild(self.convertNode(child.getChildren()[0]), 0)
        return child

class ProgramNode(AbsNode):
    children = []

    def setChild(self, child: AbsNode, index: int = 0):
        self.children[index] = child

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

    def setChild(self, child, index: int = 0):
        if index == 0:
            self.rhs = child

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
        if isinstance(self.rhs, TermNode):
            return - self.rhs.getValue()
        else:
            return self


class UnNotNode(UnOpNode):
    def __init__(self, rhs, parent=None):
        super().__init__(rhs, parent)

    def toString(self):
        return "!"

    def fold(self):
        super().fold()
        if isinstance(self.rhs, TermNode):
            return TermIntNode(not self.rhs.value)
        else:
            return self


class BinOpNode(AbsNode):
    lhs: TermNode
    rhs: TermNode

    def setChild(self, child, index: int = 0):
        if index == 0:
            self.lhs = child
        elif index == 1:
            self.rhs = child

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
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() + self.rhs.getValue()
        else:
            return self


class BinMinNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "-"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() - self.rhs.getValue()
        else:
            return self


class BinMulNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "*"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() * self.rhs.getValue()
        else:
            return self


class BinDisNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "/"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() / self.rhs.getValue()
        else:
            return self


class BinLTNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "<"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() < self.rhs.getValue()
        else:
            return self


class BinEQNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "=="

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() == self.rhs.getValue()
        else:
            return self


class BinGTNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return ">"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() > self.rhs.getValue()
        else:
            return self


class BinGTENode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent=None)

    def toString(self):
        return ">="

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() >= self.rhs.getValue()
        else:
            return self


class BinLTENode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "<="

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() <= self.rhs.getValue()
        else:
            return self


class BinNENode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "!="

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() != self.rhs.getValue()
        else:
            return self


class BinModNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "%"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() % self.rhs.getValue()
        else:
            return self


class BinAndNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "&&"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() & self.rhs.getValue()
        else:
            return self


class BinOrNode(BinOpNode):
    def __init__(self, lhs, rhs, parent=None):
        super().__init__(lhs, rhs, parent)

    def toString(self):
        return "||"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() | self.rhs.getValue()
        else:
            return self


class VariableNode(AbsNode):
    _name: str
    _index: int
    _child: TermNode = None
    const: bool = False
    _convertfunction = None

    def __str__(self):
        return str(self._child)

    def replaceConst(self):
        self._child.replaceConst()
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

    def convertNode(self):
        nchild = self._convertfunction(self._child)
        # nchild.addMetaData(self._child.getMetaData())
        return self.setChild(nchild)

    def setChild(self, child: TermNode, index: int = 0):
        if not self.const:
            self._child = child
        else:
            raise ConstException(varname=self._name, metadata=child._metadata)

    def getChildren(self):
        return [self._child]

    def fold(self):
        self._child = self._child.fold()
        return self

    def __init__(self, name: str, child: TermNode, parent=None):
        super().__init__(parent)
        self._child = child
        self._name = name
        self._convertfunction = self._child.convertNode

    def getName(self):
        return self._name

    def toString(self):
        string = ""
        if self.const:
            string += "const "
        string += self.getType() + " " + self.getName() + str(self._index)
        return string

    def getValue(self):
        return self

    def getType(self):
        return ""



class FunctionNode(AbsNode):
    functionName:str
    parameters:list

    def __init__(self,name,parameters):
        super().__init__()
        self.functionName = name
        self.parameters = parameters

class PrintfNode(FunctionNode):

    def __init__(self,parameters):
        super().__init__("printf",parameters)

    def toString(self):
        return "printf(" + str(self.parameters[0]) + ")"

class VariableIntNode(VariableNode):
    def __init__(self, name: str, child: TermIntNode = TermIntNode(), parent=None):
        super().__init__(name, child, parent)

    def getType(self):
        return "int"


class VariableFloatNode(VariableNode):
    def __init__(self, name: str, child: TermFloatNode = TermFloatNode(), parent=None):
        super().__init__(name, child, parent)

    def getType(self):
        return "float"


class VariableCharNode(VariableNode):
    def __init__(self, name: str, child: TermCharNode = TermCharNode(), parent=None):
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

    def setChild(self, child: TermNode, index: int = 0):
        self.pointTo(child)

    def pointTo(self, child: TermNode or VariableNode):
        if type(child) == self.point_to_type:
            self._child = child

    def getChildren(self):
        return [self._child]

    def convertNode(self):
        nchild = self._convertfunction()
        # nchild.addMetaData(self._child.getMetaData())
        return self.setChild(nchild)