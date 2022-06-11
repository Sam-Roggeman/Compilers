import copy

from Nodes.AbsNode import AbsNode
from Nodes.TermNodes import TermCharNode
from Nodes.VariableNodes import PointerNode, ir

class ArrayRefNode(PointerNode):
    index: AbsNode
    def getSolvedType(self) -> type:
        return self.point_to_type().getSolvedType()

    def __init__(self,arr_name,index, pointee):
        super().__init__(pointee)
        self._name = arr_name
        self.index = index

    def getChildren(self):
        return super(ArrayRefNode, self).getChildren() + [self.index]


    def __str__(self):
        return f'{self._name}[{self.index}]'

class ArrayNode(PointerNode):
    arr: list
    def __init__(self, node, ln):
        super().__init__(node)
        self.arr = [copy.deepcopy(node) for i in range(ln)]
    def getLLVMType(self):
        return ir.ArrayType(self.point_to_type().getLLVMType(),len(self.arr))

    def __getitem__(self, key):
        return self.arr[key]

    def __setitem__(self, key, value):
        self.arr[key] = value

    def setParent(self, parent):
        self.parent = parent

    def getChildren(self):
        return self.arr


class StringNode(ArrayNode):

    def __init__(self, string):
        super().__init__(TermCharNode(),len(string))
        for index in range(len(string)):
            self[index] = TermCharNode(string[index])

    def getFullString(self):
        returnval = ''
        for el in self.arr:
            returnval += el.value
        return returnval
