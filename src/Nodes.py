import sys

from Errors import *
from llvmlite import ir

# Create some useful types
cfloat = ir.DoubleType()
i32 = ir.IntType(32)
cchar = ir.IntType(8)
cbool = ir.IntType(1)


class TermNode: pass


def richest(node1: type, node2: type):
    types = [
        TermFloatNode,
        TermIntNode,
        TermCharNode
    ]
    for t in types:
        if t == node1 or t == node2:
            return t


class AbsNode:

    def setRvalue(self):
        self.rvalue = True

    def isRvalue(self):
        return self.rvalue

    def countUsages(self, rhcounter=None, lhcounter=None):
        if lhcounter is None:
            lhcounter = dict()
        if rhcounter is None:
            rhcounter = dict()
        children = self.getChildren()
        for index in range(len(children)):
            lhcounter, rhcounter = children[index].countUsages(lhcounter=lhcounter, rhcounter=rhcounter)
        return lhcounter, rhcounter

    def __str__(self):
        return self.toString()

    def setParent(self, parent):
        self.parent = parent

    def removeChild(self, index):
        pass

    def removeUnUsed(self):
        children = self.getChildren()
        for index in range(len(children) - 1, 0, -1):
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
        self._metadata: MetaData
        self._lvalue = True
        self.rvalue = False
        self.symbol_table = None

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

    def solveTypes(self):
        children = self.getChildren()
        for index in range(len(children)):
            children[index].solveTypes()


class TermNode(AbsNode):
    def getSolvedType(self) -> type:
        return type(self)

    @staticmethod
    def getLLVMType():
        pass

    def checkParent(self, parent):
        if not self.parent:
            self.setParent(parent)

    def __str__(self):
        return str(self.value)

    def setValue(self, value):
        if value:
            self.value = value

    def getValue(self):
        return self

    @staticmethod
    def convertNode(child):
        return child

    def __init__(self, value=None):
        super().__init__()
        self.value = None
        self.setValue(value)
        self._lvalue = False

    def __invert__(self):
        if self.value:
            return TermIntNode(1)
        return TermIntNode(0)

    def __add__(self, other):
        # richest_type = richest(type(self),type(other))
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
        if self.value and other.value:
            return TermIntNode(1)
        return TermIntNode(0)

    def __or__(self, other):
        other = self.convertNode(other)
        if self.value or other.value:
            return TermIntNode(1)
        return TermIntNode(0)

    # def __bool__(self):
    #     return self.value == 0

    def fold(self):
        return self

    def llvmValue(self):
        pass


class TermIntNode(TermNode):
    def __truediv__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value // other.value)
        return self

    def llvmValue(self):
        return ir.Constant(i32, self.value)

    def __init__(self, value: int = None):
        super().__init__()
        self.setValue(value)

    def setValue(self, value: int):
        if value is not None:
            if isinstance(value, bool):
                if value:
                    self.value = 1
                    return
                self.value = 0
                return
            self.value = int(value)
    def toString(self):
        return "i32" + str(self.value)

    @staticmethod
    def convertNode(child: TermNode):
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
        return child

    @staticmethod
    def getLLVMType():
        return i32


class TermFloatNode(TermNode):
    def llvmValue(self):
        return ir.Constant(cfloat, self.value)

    def __init__(self, value: float = None):
        super().__init__(value)

    def setValue(self, _value: float):
        _value = float(_value)

        super().setValue(_value)

    def toString(self):
        return "cfloat" + str(self.value)

    @staticmethod
    def convertNode(child: TermNode):
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
        return child

    @staticmethod
    def getLLVMType():
        return cfloat


class TermCharNode(TermNode):
    @staticmethod
    def getLLVMType():
        return cchar

    def llvmValue(self):
        intvalue = ord(self.value)

        return ir.Constant(cchar, intvalue)

    def setValue(self, _value: str):
        _value = str(_value)

        if len(_value) == 1:
            super().setValue(_value)

    def __init__(self, value: str = None):
        super().__init__(value)

    def toString(self):
        return "cchar" + str(self.value)

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
        return child


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

    def countUsages(self, rhcounter: [str, int] = dict(), lhcounter: [str, int] = dict()):
        if self._name:
            if self.getName() not in lhcounter.keys():
                lhcounter[self.getName()] = 0
            if self.getName() not in rhcounter.keys():
                rhcounter[self.getName()] = 0

            node = self
            while not isinstance(node.parent, AssNode):
                if isinstance(node.parent, StatementNode):
                    break
                node = node.parent
            if isinstance(node.parent, StatementNode):
                return super().countUsages(rhcounter=rhcounter, lhcounter=lhcounter)
            elif node.parent.getChildren()[0] == node:
                lhcounter[self.getName()] += 1
            else:
                rhcounter[self.getName()] += 1
        return super().countUsages(rhcounter=rhcounter, lhcounter=lhcounter)


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


class FunctionNode(AbsNode):
    functionName: str

    def __init__(self, name):
        super().__init__()
        self.functionName = name
        self.argumentNode: ArgumentsNode = ArgumentsNode()

    def addArgument(self, child):
        self.argumentNode = child

    def getChildren(self):
        return [self.argumentNode]

    def fold(self):
        self.argumentNode = self.argumentNode.fold()
        return self

class FunctionCall(FunctionNode):
    def __init__(self,name):
        super().__init__(name)

    def toString(self):
        return "Functioncall" + " " +  self.functionName

class FunctionDefinition(FunctionNode):

    def __init__(self,name,type):
        super().__init__(name)
        self.functionbody = None
        self.type = type
        self.symbol_table = SymbolTable()

    def getSymbolTable(self):
        return self.symbol_table

    def setSymbolTabel(self, symboltable):
        self.symbol_table = symboltable

    def setFunctionbody(self,body):
        self.functionbody = body

    def checkParent(self,parent):
        self.parent = parent
        if self.argumentNode:
            self.argumentNode.checkParent(self)
        if self.functionbody:
            self.functionbody.checkParent(self)

    def toString(self):
        return self.type + " " + self.functionName

    def getChildren(self):
        if not self.argumentNode and self.functionbody:
            return [ self.functionbody]
        elif not self.functionbody and self.argumentNode:
            return [self.argumentNode]
        elif not self.functionbody and not self.argumentNode:
            return []
        else:
            return [self.argumentNode,self.functionbody]

class FunctionBody(AbsNode):
    def __init__(self):
        super().__init__("FunctionBody")
        self.body = []

    def toString(self):
        return "functionbody"

    def checkParent(self,parent):
        self.parent = parent
        for c in self.body:
            c.setParent(self)

    def addBody(self,body):
        self.body.append(body)

    def getChildren(self):
        return self.body

class ReturnNode(AbsNode):
    def __init__(self):
        super().__init__("return")
        self.child = None

    def getChildren(self):
        return [self.child]

    def toString(self):
        return "return"

    def setChild(self, child, index: int = 0):
        self.child = child

class PrintfNode(FunctionNode):

    def __init__(self):
        super().__init__("printf")

    def toString(self):
        return "printf"

    def checkParent(self, parent=None):
        if parent:
            self.parent = parent
            for c in self.getChildren():
                c.checkParent(self)


class ArgumentsNode(AbsNode):

    def __init__(self):
        super().__init__("Arguments")
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def checkParent(self, parent=None):
        if parent:
            self.parent = parent
        for c in self.getChildren():
            c.setParent(self)

    def getChildren(self):
        return self.children

    def toString(self):
        return "Arguments"

    def fold(self):
        for index in range(len(self.children)):
            self.children[index] = self.children[index].fold()
        return self


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


class VariableEntry(object):
    const: bool
    type: type
    node: VariableNode
    value: TermNode
    register: str
    lhscounter: int
    rhscounter: int

    def __init__(self):
        self.const = False
        self.lhscounter = 0
        self.rhscounter = 0

    def setcounters(self, lhs, rhs):
        self.lhscounter = lhs
        self.rhscounter = rhs

    def getNode(self):
        return self.node

    def setConst(self):
        self.const = True

    def getConst(self):
        return self.node.isConst()


class SymbolTable:
    # dict[str, VariableEntry]
    variables = dict()

    def __init__(self):
        self.children = []
        self.parent = None
        self.variables = dict()

    def getValue(self, varname):
        tableEntry = self.getTableEntry(varname)
        return tableEntry.value

    def append(self, node: VariableNode):
        if not node.getName() in self.variables:
            self.variables[node.getName()] = VariableEntry()
        self.variables[node.getName()].node = node

    def setParent(self, parent):
        self.parent = parent

    def addChild(self, child):
        child.setParent(self)
        self.children.append(child)

    def getVar(self, varname):
        if varname not in self.variables:
            if self.parent:
                return self.parent.getVar(varname)
            raise UninitializedException(varname=varname)

        return self.variables[varname].node

    def getConst(self, key):
        tableEntry = self.getTableEntry(key)
        return tableEntry.getConst()

    # def getVariables(self, keys):
    #     tableEntry = self.getTableEntry(keys)
    #     return self.variables[keys]

    def removeVar(self, varnode: VariableNode):
        if varnode.getName() not in self.variables:
            if self.parent:
                return self.parent.removeVar(varnode)
            raise UninitializedException(varname=varnode.getName())
        self.variables.pop(varnode.getName())

    def makeConst(self, key):
        tableEntry = self.getTableEntry(key)
        tableEntry.node.makeConst()
        tableEntry.setConst()

    def setValue(self, name, node2):
        tableEntry = self.getTableEntry(name)
        tableEntry.value = node2

    def getTableEntry(self, name):
        if name not in self.variables:
            if self.parent:
                return self.parent.getTableEntry(name)
            raise UninitializedException(varname=name)

        return self.variables[name]

    def foundRHS(self, name):
        tableEntry = self.getTableEntry(name)
        tableEntry.rhscounter += 1

    def foundLHS(self, name):
        tableEntry = self.getTableEntry(name)
        tableEntry.lhscounter += 1

    def setConst(self):
        for value in self.variables.values():
            lhscounter = value.lhscounter
            rhscounter = value.rhscounter
            if rhscounter != 0 and lhscounter == 0:
                pass
            elif lhscounter == 1:
                value.node.makeConst()


class CodeblockNode(AbsNode):

    def checkParent(self, parent=None):
        if parent:
            self.parent = parent
        for c in self.getChildren():
            c.checkParent(self)

    def setChild(self, child: AbsNode, index: int = 0):
        child.setParent(self)
        self.children[index] = child

    def getSymbolTable(self):
        return self.symbol_table

    def setSymbolTabel(self, symboltable):
        self.symbol_table = symboltable

    def __init__(self):
        super().__init__()
        self.children = []
        self.symbol_table = SymbolTable()

    def addchild(self, child):
        child.setParent(self)
        self.children.append(child)

    def getChildren(self):
        return self.children

    def removeChild(self, index):
        self.children.pop(index)

    def toString(self):
        return "Codeblock"

    def fold(self):
        for index in range(len(self.children)):
            self.children[index] = self.children[index].fold()
        return self


class ProgramNode(CodeblockNode):
    def __init__(self):
        super().__init__()

    def toString(self):
        return "Program"


class UnOpNode(AbsNode):

    def checkParent(self, parent):
        self.setParent(parent)
        for c in self.getChildren():
            c.checkParent(self)

    def setChild(self, child, index: int = 0):
        if index == 0:
            self.rhs = child
            self.rhs.setParent(self)

    def getChildren(self):
        return [self.rhs]

    def __init__(self):
        super().__init__()
        self.rhs = None

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
            if not self.rhs.value:
                return TermIntNode(1)
            return TermIntNode(0)
        return self


class BinOpNode(AbsNode):
    lhs: TermNode
    rhs: TermNode
    type: type

    def getSolvedType(self) -> type:
        return self.type

    def solveTypes(self):
        AbsNode.solveTypes(self)

        self.type = richest(self.lhs.getSolvedType(), self.rhs.getSolvedType())

    def checkParent(self, parent):
        self.setParent(parent)
        for c in self.getChildren():
            c.checkParent(self)

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
        self.lhs: TermNode
        self.rhs: TermNode

    def fold(self):
        self.lhs = self.lhs.fold()
        self.rhs = self.rhs.fold()
        return self

    def getLLVMType(self):
        return self.type().getLLVMType()


class TermBoolNode(TermNode):
    def __init__(self):
        super().__init__(False)

    @staticmethod
    def getLLVMType():
        return cbool

    def getSolvedType(self) -> type:
        return TermBoolNode


class BinLogOpNode(BinOpNode):
    def __init__(self):
        super(BinLogOpNode, self).__init__()
        self.type = TermBoolNode

    # def solveTypes(self):
    #     AbsNode.solveTypes(self)


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


class BinAndNode(BinLogOpNode):
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


class RefNode(AbsNode):
    child: VariableNode

    def getChildren(self):
        return [self.child]

    def checkParent(self, parent):
        self.setParent(parent)
        self.child.setParent(self)

    def toString(self):
        return "&"

    def toDot(self, dot):
        dot.node(str(id(self)), str(self))
        self.child.toDot(dot)
        dot.edge(str(id(self)), str(id(self.child)))
        return dot

    def preOrderTraversal(self, string: str, oneline=True, indent=0):
        if oneline:
            string += self.toString() + ","
            c = self.getChildren()
            string += self.child.getName() + ","
        else:
            for i in range(0, indent):
                string += '\t'
            string += self.toString()
            string += '\n'
            for child in self.getChildren():
                string = child.preOrderTraversal(string, oneline, indent + 1)
        return string

    def setChild(self, child, index: int = 0):
        self.child = child
        self.child.setParent(self)

    def __init__(self):
        super().__init__()


class AssNode(BinOpNode):
    lhs: VariableNode

    def solveTypes(self):
        AbsNode.solveTypes(self)
        self.type = self.lhs.getSolvedType()
        if isinstance(self.rhs, TermNode) and self.type != self.rhs.getSolvedType():
            self.rhs = self.type(self.rhs.value)
        return

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
    _name = None

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

    def pointTo(self, child: TermNode or VariableNode or StringNode):
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


class StatementNode(AbsNode):

    def __init__(self):
        super().__init__()
        self.block = None
        self.children = []
        self.symbol_table = None

    def setBlock(self, block):
        self.block = block

    def getSymbolTable(self):
        return self.symbol_table

    def setSymbolTabel(self, symboltable):
        self.symbol_table = symboltable

    def getChildren(self):
        return self.children

    def addChild(self, child):
        self.children.append(child)

    def checkParent(self, parent):
        self.setParent(parent)
        for c in self.getChildren():
            c.checkParent(self)

    def toString(self):
        return "statement"


class IfstatementNode(StatementNode):
    condition: AbsNode

    def __init__(self):
        super().__init__()

    def setCondition(self, condition):
        self.condition = condition

    def getChildren(self):
        return [self.condition, self.block]

    def toString(self):
        return "if"


class ElsestatementNode(StatementNode):

    def __init__(self):
        super().__init__()

    def getChildren(self):
        return [self.block]

    def toString(self):
        return "else"


class WhilestatementNode(StatementNode):
    condition: AbsNode

    def __init__(self):
        super().__init__()

    def setCondition(self, condition):
        self.condition = condition

    def getChildren(self):
        return [self.condition, self.block]

    def toString(self):
        return "while"


class ForstatementNode(WhilestatementNode):

    def __init__(self):
        super().__init__()

    def addChild(self, child):
        child.setParent(self)
        self.children = []
        self.children.append(child)

    def toString(self):
        return "for"


class ConditionNode(AbsNode):

    def __init__(self):
        super().__init__()
        self.children = []
        parent = None

    def toString(self):
        return "condition"

    def getChildren(self):
        return self.children

    def addChild(self, child):
        child.setParent(self)
        self.children.append(child)

    def checkParent(self, parent):
        self.setParent(parent)
        for c in self.getChildren():
            c.checkParent(self)


class BreakNode(TermNode):
    def __init__(self):
        super().__init__("break")


class ContinueNode(TermNode):
    def __init__(self):
        super().__init__("continue")

class IncludeNode(AbsNode):
    def __init__(self):
        super().__init__("include")
        self.library = None

    def setLibrary(self,library):
        self.library = library

    def getChildren(self):
        return [self.library]

    def checkParent(self,parent):
        self.parent = parent
        self.library.setParent(self)

    def toString(self):
        return "#include"

class LibraryNode(AbsNode):
    def __init__(self,name):
        super().__init__(name)
        self.name = name

    def setParent(self, parent):
        self.parent = parent

    def toString(self):
        return self.name