import graphviz
from SymbolTable import *


class AST:
    # todo parent

    _name = "output"
    _root: ProgramNode
    _working_node = None
    _last_entered_treenode = None
    _symbol_table: SymbolTable = SymbolTable()

    def __init__(self, root: ProgramNode, name):
        self._name = name
        self._root = root

    # def __init__(self, tree, name=None):
    #     self._name = name
    #     try:
    #         self._root = self.FindOp(tree)
    #     except GeneralException as e:
    #         tree = self._last_entered_treenode
    #         e.setMetaData(metadata=MetaData(line=tree.start.line,start_character=tree.start.column))
    #         raise e

    def toDot(self, name: str, d_format="png"):
        dot = graphviz.Digraph(self._name, comment=self._name, strict=True)
        dot = self._root.toDot(dot)
        dot.render(filename="./output/" + self._name + "/" + name, format=d_format)
        return

    def fold(self):
        self._root.fold()

    def preOrderTraversal(self, oneline=True):
        string = ""
        string = self._root.preOrderTraversal(string, oneline)[:-1]
        return string

    def findNode(self, name: str):
        deref_count = 0
        for c in name:
            if c == '*':
                deref_count = + 1
            else:
                break
        name = name[deref_count:]
        s = self._symbol_table.getCurrentVar(varname=name)
        for i in range(0, deref_count):
            s = s.deRef()
        return s

    def replaceConst(self):
        self._symbol_table.replaceConst()
        # self._root = self._root.replaceConst()

    def optimize(self):
        self.toDot(name="start")
        self.replaceConst()
        self._symbol_table.reIndex()
        # self.toDot(name="after_const")
        self.fold()
        self.toDot(name="end")
