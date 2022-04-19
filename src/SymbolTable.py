from Nodes import *


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
        for c in self.children:
            c.setConst()
