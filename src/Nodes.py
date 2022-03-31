import sys

from Errors import *



class AbsNode():
    parent = None
    _metadata: MetaData
    _lvalue = True

    def countUsages(self, rhcounter: [str, int] = dict(), lhcounter: [str, int]= dict()):
        children = self.getChildren()
        for index in range(len(children)):
            if index == 2:
                a = 5
            lhcounter, rhcounter = children[index].countUsages(lhcounter=lhcounter,rhcounter=rhcounter)
        return lhcounter, rhcounter

    def __str__(self):
        return self.toString()

    def setParent(self, parent):
        self.parent = parent

    def removeChild(self,index):
        pass

    def removeUnUsed(self):
        children = self.getChildren()
        for index in range(len(children)-1,0,-1):
            if children[index].checkUnUsed():
                self.removeChild(index)

    def checkUnUsed(self):
        return False

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
        return False

    def __init__(self, parent=None):
        self.parent = parent

    def toString(self):
        return ""

    def fold(self):
        return self

    def getChildren(self):
        return []

    def toDot(self, dot):
        dot.node(str(id(self)), str(self))
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

    def __init__(self, value):
        super().__init__()
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

    def __init__(self, value: int = None):
        super().__init__(value)

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
            # nchild.addMetaData(child.getMetaData())
            return nchild
        elif isinstance(child, TermCharNode):
            nchild = TermIntNode(ord(child.value))
            # nchild.addMetaData(child.getMetaData())
            return nchild
        elif len(child.getChildren()) != 0:
            child.setChild(self.convertNode(child.getChildren()[0]), 0)
        return child


class TermFloatNode(TermNode):

    def __init__(self, value: float = None):
        super().__init__(value)

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
            # nchild.addMetaData(child.getMetaData())
            return nchild

        elif isinstance(child, TermCharNode):
            nchild = TermFloatNode(float(ord(child.value)))
            nchild.addMetaData(child.getMetaData())
            return nchild
        elif len(child.getChildren()) != 0:
            child.setChild(self.convertNode(child.getChildren()[0]), 0)
        return child


class TermCharNode(TermNode):

    def setValue(self, _value: str):
        _value = str(_value)

        if len(_value) == 1:
            super().setValue(_value)

    def __init__(self, value: str = None):
        super().__init__(value)

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
            # nchild.addMetaData(child.getMetaData())
            return nchild
        elif isinstance(child, TermIntNode):
            sys.stderr.write("Warning: Implicit conversion from int to char, possible loss of information " + "\n")
            nchild = TermCharNode(chr(child.value))
            # nchild.addMetaData(child.getMetaData())
            return nchild
        elif len(child.getChildren()) != 0:
            child.setChild(self.convertNode(child.getChildren()[0]), 0)
        return child


class ProgramNode(AbsNode):
    children = []

    def setChild(self, child: AbsNode, index: int = 0):
        child.setParent(self)
        self.children[index] = child

    def __init__(self):
        super().__init__()

    def addchild(self, child):
        child.setParent(self)
        self.children.append(child)

    def getChildren(self):
        return self.children

    def removeChild(self,index):
        self.children.pop(index)

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
            self.rhs.setParent(self)

    def getChildren(self):
        return [self.rhs]

    def __init__(self):
        super().__init__()

    def fold(self):
        self.rhs = self.rhs.fold()


class UnPlusNode(UnOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "+"

    def fold(self):
        super().fold()
        return self.rhs.getValue()


class UnMinNode(UnOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "-"

    def fold(self):
        super().fold()
        if isinstance(self.rhs, TermNode):
            return - self.rhs.getValue()
        else:
            return self


class UnNotNode(UnOpNode):
    def __init__(self):
        super().__init__()

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
            self.lhs.parent = self
        elif index == 1:
            self.rhs = child
            self.rhs.parent = self

    def setChildren(self, lhs, rhs):
        self.lhs = lhs
        self.lhs.setParent(self)
        self.rhs = rhs
        self.rhs.setParent(self)

    def getChildren(self):
        return [self.lhs, self.rhs]

    def __init__(self):
        super().__init__()

    def fold(self):
        self.lhs = self.lhs.fold()
        self.rhs = self.rhs.fold()
        return self


class BinPlusNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "+"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() + self.rhs.getValue()
        else:
            return self


class BinMinNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "-"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() - self.rhs.getValue()
        else:
            return self


class BinMulNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "*"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() * self.rhs.getValue()
        else:
            return self


class BinDisNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "/"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() / self.rhs.getValue()
        else:
            return self


class BinLTNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "<"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() < self.rhs.getValue()
        else:
            return self


class BinEQNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "=="

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() == self.rhs.getValue()
        else:
            return self


class BinGTNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return ">"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() > self.rhs.getValue()
        else:
            return self


class BinGTENode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return ">="

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() >= self.rhs.getValue()
        else:
            return self


class BinLTENode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "<="

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() <= self.rhs.getValue()
        else:
            return self


class BinNENode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "!="

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() != self.rhs.getValue()
        else:
            return self


class BinModNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "%"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() % self.rhs.getValue()
        else:
            return self


class BinAndNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "&&"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() & self.rhs.getValue()
        else:
            return self


class BinOrNode(BinOpNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "||"

    def fold(self):
        super().fold()
        if isinstance(self.lhs, TermNode) and isinstance(self.rhs, TermNode):
            return self.lhs.getValue() | self.rhs.getValue()
        else:
            return self


class VariableNameNode(AbsNode):
    _name: str

    def setName(self, name: str):
        self._name = name

    def getName(self):
        return self._name

    def __str__(self):
        return self.toString()


    def toString(self):
        return self.getName()

    def countUsages(self, rhcounter: [str, int] = dict(), lhcounter: [str, int]= dict()):
        if self.getName() not in lhcounter.keys():
            lhcounter[self.getName()] = 0
        if self.getName() not in rhcounter.keys():
            rhcounter[self.getName()] = 0

        node = self
        while not isinstance(node.parent, AssNode):
            node = node.parent

        if node.parent.getChildren()[0] == node:
            lhcounter[self.getName()] += 1
        else:
            rhcounter[self.getName()] += 1
        return super().countUsages(rhcounter=rhcounter, lhcounter=lhcounter)

class VariableNode(VariableNameNode):
    const: bool = False
    no_use: bool = False
    _convertfunction = None

    def __str__(self):
        return super().__str__()

    def makeConst(self):
        self.const = True

    def isConst(self):
        return self.const

    def copy(self):
        return copy.deepcopy(self)

    def unUsed(self):
        self.no_use = True

    def isUnUsed(self):
        return self.no_use

    # def convertNode(self):
        # nchild = self._convertfunction(self._child)
        # nchild.addMetaData(self._child.getMetaData())
        # return self.setChild(nchild)

    def fold(self):
        return self

    def __init__(self):
        super().__init__()
        # self._convertfunction = self._child.convertNode

    def toString(self):
        string = ""
        if self.const:
            string += "const "
        string += self.getType() + " " + self.getName()
        return string

    def getValue(self):
        return self

    def getType(self):
        return ""


class FunctionNode(AbsNode):
    functionName: str
    parameters: list

    def __init__(self, name, parameters):
        super().__init__()
        self.functionName = name
        self.parameters = parameters


class PrintfNode(FunctionNode):

    def __init__(self, parameters):
        super().__init__("printf", parameters)

    def toString(self):
        return "printf(" + str(self.parameters[0]) + ")"


class VariableIntNode(VariableNode):
    def __init__(self):
        super().__init__()

    def getType(self):
        return "int"


class VariableFloatNode(VariableNode):
    def __init__(self):
        super().__init__()

    def getType(self):
        return "float"


class VariableCharNode(VariableNode):
    def __init__(self):
        super().__init__()

    def getType(self):
        return "char"


class RefNode(AbsNode):
    child: VariableNode

    def setChild(self, child, index: int = 0):
        self.child = child
        self.child.setParent(self)

    def __init__(self):
        super().__init__()


class AssNode(BinOpNode):

    lhs: VariableNode

    def __init__(self):
        super().__init__()

    def toString(self):
        return "="

    def checkUnUsed(self):
        return self.lhs.isUnUsed()

    def replaceConst(self):
        if self.lhs.isConst():
            return self.rhs

        else:
            return self

    def __str__(self):
        return "="


class PointerNode(VariableNode):
    point_to_type: type

    def __init__(self, child: TermNode or VariableNode):
        super().__init__(child)
        self.point_to_type = type(child)

    def toString(self):
        return self._name + "*"

    def deRef(self):
        return self._child

    def setChild(self, child: TermNode, index: int = 0):
        self.pointTo(child)
        self._child.setParent(self)

    def pointTo(self, child: TermNode or VariableNode):
        if type(child) == self.point_to_type:
            self._child = child

    def getChildren(self):
        return [self._child]

    def convertNode(self):
        # nchild = self._convertfunction()
        # nchild.addMetaData(self._child.getMetaData())
        return self
