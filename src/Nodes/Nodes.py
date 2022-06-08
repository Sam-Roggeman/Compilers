from Nodes.FunctionNodes import *
from Nodes.VariableNodes import *
from SymbolTable import *

def richest(node1: type, node2: type):
    types = [
        TermFloatNode,
        TermIntNode,
        TermCharNode
    ]
    for t in types:
        if t == node1 or t == node2:
            return t


class VariableEntry(object):
    const: bool
    type: type
    node: VariableNode
    value: TermNode
    register = None
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


# class SymbolTable:
#     # dict[str, VariableEntry]
#     variables = dict()
#     functions = dict()
#
#     def __init__(self):
#         self.children = []
#         self.parent = None
#         self.variables = dict()
#         self.functions = dict()
#
#     def getValue(self, varname):
#         tableEntry = self.getTableEntry(varname)
#         return tableEntry.value
#
#     def nodeCheck(self, node):
#         if not node.getName() in self.variables.keys():
#             if self.parent:
#                 return self.parent.nodeCheck(node)
#             return True
#         raise RedefinitionException(varname=node.getName())
#
#     def getFunction(self, node):
#         if not node.getName() in self.functions.keys():
#             if self.parent:
#                 return self.parent.getFunction(node)
#             return False
#         return True
#
#     def functionnodeCheck(self, node):
#         if not node.getName() in self.functions.keys():
#             if self.parent:
#                 return self.parent.functionnodeCheck(node)
#             return True
#         c = self.functions[node.getName()].getArguments()
#         if len(node.getArguments().getChildren()) != 0 and c:
#             if c.getChildren()[0].getType() == node.getArguments().getChildren()[0].getType():
#                 raise FunctionRedefinitionException(varname=node.getName())
#         return True
#
#     def append(self, node: VariableNode):
#         if self.nodeCheck(node):
#             if not node.getName() in self.variables:
#                 self.variables[node.getName()] = VariableEntry()
#             self.variables[node.getName()].node = node
#
#     def appendFunction(self, node: FunctionNode):
#         if self.functionnodeCheck(node):
#             if not node.getName() in self.functions:
#                 self.functions[node.getName()] = FunctionEntry()
#             self.functions[node.getName()].node = node
#
#     def setParent(self, parent):
#         self.parent = parent
#
#     def addChild(self, child):
#         child.setParent(self)
#         self.children.append(child)
#
#     def getVar(self, varname):
#         if varname not in self.variables:
#             if self.parent:
#                 return self.parent.getVar(varname)
#             raise UninitializedException(varname=varname)
#
#         return self.variables[varname].node
#
#     def getConst(self, key):
#         tableEntry = self.getTableEntry(key)
#         return tableEntry.getConst()
#
#     # def getVariables(self, keys):
#     #     tableEntry = self.getTableEntry(keys)
#     #     return self.variables[keys]
#
#     def removeVar(self, varnode: VariableNode):
#         if varnode.getName() not in self.variables:
#             if self.parent:
#                 return self.parent.removeVar(varnode)
#             raise UninitializedException(varname=varnode.getName())
#         self.variables.pop(varnode.getName())
#
#     def makeConst(self, key):
#         tableEntry = self.getTableEntry(key)
#         tableEntry.node.makeConst()
#         tableEntry.setConst()
#
#     def setValue(self, name, node2):
#         tableEntry = self.getTableEntry(name)
#         tableEntry.value = node2
#
#     def getTableEntry(self, name):
#         if name not in self.variables:
#             if self.parent:
#                 return self.parent.getTableEntry(name)
#             raise UninitializedException(varname=name)
#
#         return self.variables[name]
#
#     def foundRHS(self, name):
#         tableEntry = self.getTableEntry(name)
#         tableEntry.rhscounter += 1
#
#     def foundLHS(self, name):
#         tableEntry = self.getTableEntry(name)
#         tableEntry.lhscounter += 1
#
#     def setConst(self):
#         for value in self.variables.values():
#             lhscounter = value.lhscounter
#             rhscounter = value.rhscounter
#             if rhscounter != 0 and lhscounter == 0:
#                 pass
#             elif lhscounter == 1:
#                 value.node.makeConst()
#         for c in self.children:
#             c.setConst()


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
        a = self.type.getLLVMType()
        return a


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
            sys.stderr.write(f"Implicit conversion from {self.rhs.getSolvedType().getType()} to {self.type.getType()}")
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


class StatementNode(AbsNode):
    def __init__(self):
        super().__init__()
        self.block = None
        self.children = []
        self.symbol_table = SymbolTable()

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


class IfElseStatementNode(IfstatementNode):
    else_statement: ElsestatementNode

    def __init__(self, ifnode: IfstatementNode, elsenode: ElsestatementNode):
        super().__init__()
        self.block = ifnode.block
        self.condition = ifnode.condition
        self.else_statement = elsenode

    def getChildren(self):
        return [self.condition, self.block, self.else_statement.block]

    def toString(self):
        return "if_else"


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

    def setLibrary(self, library):
        self.library = library

    def getChildren(self):
        return [self.library]

    def checkParent(self, parent):
        self.parent = parent
        self.library.setParent(self)

    def toString(self):
        return "#include"


class LibraryNode(AbsNode):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def setParent(self, parent):
        self.parent = parent

    def toString(self):
        return self.name
