from Nodes import *


class VariableTable(list):
    def append(self, node: VariableNode):
        node.setIndex(len(self))
        super(VariableTable, self).append(node)

    def reIndex(self):
        index = 0
        for node in self:
            node.setIndex(index)
            index += 1


class SymbolTable:
    #dict[str, VariableTable]
    variables = {}

    def append(self, node: VariableNode):
        if not node.getName() in self.variables:
            self.variables[node.getName()] = VariableTable()
        self.variables[node.getName()].append(node)

    def getCurrentVar(self, varname):
        if not varname in self.variables:
            raise UninitializedException(varname=varname)

        return self.variables[varname][len(self.variables[varname]) - 1]

    def isVar(self,varname):
        if varname in self.variables.keys():
            return True
        return False

    def reIndex(self):
        for node in self.variables.values():
            node.reIndex()
    def removeVar(self, varnode:VariableNode):
        for node in self.variables[varnode.getName()]:
            if node == varnode:
                self.variables[varnode.getName()].remove(node)

    def replaceConst(self):
        for keys,values in self.variables.items():
            if len(values) == 1:
                values[0].makeConst()
                values[0].replaceConst()

