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
            raise SyntaxError("Variable \"" + varname + "\" used before initialization")

        return self.variables[varname][len(self.variables[varname]) - 1]

    def reIndex(self):
        for node in self.variables.values():
            node.reIndex()
