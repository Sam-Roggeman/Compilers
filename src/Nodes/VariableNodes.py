from Nodes.AbsNode import *
from Nodes.TermNodes import *
from llvmTypes import *


class VariableNameNode(AbsNode):
    def __init__(self):
        super().__init__()
        self._name: str = ""
        self.referenced = False

    def setReferenced(self):
        self.referenced = True

    def isReferenced(self):
        return self.referenced

    def checkParent(self, parent):
        self.setParent(parent)

    def setName(self, name: str):
        self._name = name

    def getName(self):
        return self._name

    def __str__(self):
        return self.toString()

    def toString(self):
        return self.getName()


class VariableNode(VariableNameNode):
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

    def fold(self):
        return self

    def __init__(self):
        super().__init__()
        # self._convertfunction = self._child.convertNode
        self.const: bool = False
        self.no_use: bool = False
        self._convertfunction = None

    def getSolvedType(self) -> type:
        return None

    def toString(self):
        string = ""
        if self.const:
            string += "const "
        if self._name:
            string += self.getType() + " " + self.getName()
        else:
            string += self.getType()
        return string

    def getValue(self):
        return self

    @staticmethod
    def getLLVMType():
        pass


class VariableIntNode(VariableNode):
    def __init__(self):
        super().__init__()

    def getSolvedType(self) -> type:
        return TermIntNode

    @staticmethod
    def getLLVMType():
        return i32

    def getType(self):
        return "i32"

    def getSize(self):
        return 4


class VariableFloatNode(VariableNode):
    def getSolvedType(self) -> type:
        return TermFloatNode

    def __init__(self):
        super().__init__()

    def getSize(self):
        return 4

    @staticmethod
    def getLLVMType():
        return cfloat

    def getType(self):
        return "float"


class VariableCharNode(VariableNode):
    def getSolvedType(self) -> type:
        return TermCharNode

    def __init__(self):
        super().__init__()

    def getSize(self):
        return 1

    @staticmethod
    def getLLVMType():
        return cchar

    def getType(self):
        return "char"


class PointerNode(VariableNode):
    point_to_type: type
    _name = None
    def getSize(self):
        return 4
    def getSolvedType(self) -> type:
        return type(self)

    def getLLVMType(self):
        return self._child.getLLVMType().as_pointer()

    def checkParent(self, parent):
        self.setParent(parent)
        for c in self.getChildren():
            c.checkParent(self)

    def __init__(self, child: TermNode or VariableNode):
        super().__init__()
        self.point_to_type = type(child)
        self._child = child
        self._name = None

    def toString(self):
        if not self._name:
            return "*"
        else:
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

    @staticmethod
    def convertNode(child):
        pass

    def getNode(self):
        return self.node

    def setConst(self):
        self.const = True

    def getConst(self):
        return self.node.isConst()
