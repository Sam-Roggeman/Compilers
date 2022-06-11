from Nodes.VariableNodes import VariableNode
from Nodes.TermNodes import TermNode
from Nodes.AbsNode import AbsNode
from Errors import *


class VariableEntry(object):
    const: bool
    type: type
    node: VariableNode
    value: TermNode
    register = None
    lhscounter: int
    rhscounter: int
    declared: bool

    def __init__(self):
        self.const = False
        self.lhscounter = 0
        self.rhscounter = 0
        self.declared = False

    def setcounters(self, lhs, rhs):
        self.lhscounter = lhs
        self.rhscounter = rhs

    def getNode(self):
        return self.node

    def setConst(self):
        self.const = True

    def getConst(self):
        return self.node.isConst()


class FunctionEntry(object):
    const: bool
    type: type
    node: AbsNode
    memorylocation = None
    lhscounter: int
    rhscounter: int

    def __init__(self):
        self.const = False
        self.lhscounter = 0
        self.rhscounter = 0

    def setcounters(self, lhs, rhs):
        self.lhscounter = lhs
        self.rhscounter = rhs

    def getArguments(self):
        return self.node.getArguments()

    def getNode(self):
        return self.node

    def setConst(self):
        self.const = True

    def getConst(self):
        return self.node.isConst()


class SymbolTable:
    # dict[str, VariableEntry]
    variables = dict()
    functions = dict()

    def __init__(self):
        self.children = []
        self.parent = None
        self.variables = dict()
        self.functions = dict()

    def getValue(self, varname):
        tableEntry = self.getTableEntry(varname)
        return tableEntry.value

    def nodeCheck(self, node):
        if not node.getName() in self.variables.keys():
            # if self.parent:
            #     return self.parent.nodeCheck(node)
            return True
        raise RedefinitionException(varname=node.getName())

    def checkArguments(self, node):
        node_in_symboltable = self.functions[node.getName()]
        if (len(node_in_symboltable.getArguments().getChildren()) != len(node.getArguments().getChildren())):
            raise functionCallargumentMismatch("")
        a = 2

    def getFunction(self, name):
        if name not in self.functions.keys():
            if self.parent:
                return self.parent.getFunction(name)
            return None
        self.checkArguments(self.functions[name].node)
        return self.functions[name]

    def functionnodeCheck(self, node):
        if not node.getName() in self.functions.keys():
            if self.parent:
                return self.parent.functionnodeCheck(node)
            return True
        c = self.functions[node.getName()].getArguments().getChildren()
        arguments = node.getArguments().getChildren()
        node_in_symboltable = self.functions[node.getName()].node
        if node_in_symboltable.functionbody == None:
            if len(c) == len(arguments) and node.returntype == node_in_symboltable.returntype:
                for i in range(len(arguments)):
                    if (arguments[i].getType() != c[i].getType()):
                        raise (declarationDefinitionMismatch(""))
                return True
            else:
                raise (declarationDefinitionMismatch(""))
        if len(node.getArguments().getChildren()) != 0 and c:
            if c.getChildren()[0].getType() == node.getArguments().getChildren()[0].getType():
                raise FunctionRedefinitionException(varname=node.getName())
        return True

    def append(self, node: VariableNode):
        if self.nodeCheck(node):
            if not node.getName() in self.variables:
                self.variables[node.getName()] = VariableEntry()
            self.variables[node.getName()].node = node

    def appendFunction(self, node):
        if self.functionnodeCheck(node):
            if not node.getName() in self.functions:
                self.functions[node.getName()] = FunctionEntry()
            self.functions[node.getName()].node = node

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
        if name not in self.variables:
            if self.parent:
                return self.parent.setValue(name,node2)
            raise UninitializedException(varname=name)
        self.variables[name].value = node2

    def getTableEntry(self, name,lvalue=False,onlydeclared=False, metadata=MetaData() ):
        if name in self.variables and ((self.variables[name].declared or lvalue) or not onlydeclared ):
            self.variables[name].declared= self.variables[name].declared or lvalue
            return self.variables[name]
        if self.parent:
            return self.parent.getTableEntry(name,lvalue=lvalue,onlydeclared=onlydeclared,metadata=metadata)
        raise UninitializedException(varname=name, metadata=metadata)

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
        for c in self.children:
            c.setConst()
