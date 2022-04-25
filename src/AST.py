import graphviz
from SymbolTable import *
from ASTVisitor import *
from llvmVisitor import *


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
        self._symbol_table = self._root.getSymbolTable()
        self._root.solveTypes()
        self.toDot(name="AST")

        self.optimize()

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
        self._root = self._root.fold()

    def preOrderTraversal(self, oneline=True):
        string = ""
        string = self._root.preOrderTraversal(string, oneline)
        return string

    def findNode(self, name: str):
        deref_count = 0
        for c in name:
            if c == '*':
                deref_count = + 1
            else:
                break
        name = name[deref_count:]
        s = self._symbol_table.getVar(varname=name)
        for i in range(0, deref_count):
            s = s.deRef()
        return s

    def replaceConst(self, curr_node):

        children = curr_node.getChildren()
        for index in range(len(children)):
            self.replaceConst(children[curr_node])

    def optimize(self):
        self._root.checkParent()
        ASTUsageVisitor(ctx=self._root, symbol_table=self._root.symbol_table)
        # ASTConstVisitor(self.getRoot(), self.getSymbolTable(()))
        self._symbol_table.setConst()
        self.fold()
        self.toDot(name="Optimized")

    def getRoot(self):
        return self._root

    def getSymbolTable(self, param):
        return self._symbol_table

    def exportToLLVM(self, run=False):
        llvmVisitor(self._root, self._symbol_table, "./output/" + self._name + "/" + "output.llvm",run=run)
