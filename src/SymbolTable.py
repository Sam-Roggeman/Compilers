from Nodes import *


class VariableEntry(object):
    const: bool = False
    type: type
    node: VariableNode
    value:TermNode
    lhscounter = 0
    rhscounter = 0

    def setcounters(self,lhs,rhs):
        self.lhscounter = lhs
        self.rhscounter = rhs

    def getNode(self):
        return self.node

    def setConst(self):
        self.const = True

    def getConst(self):
        return self.node.isConst()

class SymbolTable:
    #dict[str, VariableTable]
    variables = dict()

    def append(self, node: VariableNode):
        if not node.getName() in self.variables:
            self.variables[node.getName()] = VariableTable()
        self.variables[node.getName()].append(node)


    def getVar(self, varname):
        if varname not in self.variables:
            raise UninitializedException(varname=varname)

        return self.variables[varname].node

    def isVar(self,varname):
        if varname in self.variables.keys():
            return True
        return False

    def getConst(self, key):
        return self.variables[key].getConst()

    def getVariables(self, keys):
        return self.variables[keys]

    def removeVar(self, varnode:VariableNode):
        for node in self.variables[varnode.getName()]:
            if node == varnode:
                self.variables[varnode.getName()].remove(node)

    def makeConst(self, key):
            self.variables[key].node.makeConst()
            self.variables[key].setConst()

    def setValue(self, name, node2):
        self.variables[name].value = node2
