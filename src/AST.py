import graphviz
from src.Nodes import *


class AST:
    # todo parent

    _name = "output"
    _dotnummer = 0
    _root = None

    def __init__(self, tree, name=None):
        self._name = name
        print(type(tree))
        print(dir(tree))
        self._root = self.FindOp(tree)

    def toDot(self, d_format="png"):
        dot = graphviz.Digraph(self._name, comment=self._name)
        dot = self._root.toDot(dot)
        dot.render(filename="./output/" + self._name + str(self._dotnummer), format=d_format)
        self._dotnummer += 1
        return

    def FindOp(self, tree):
        node = None
        if hasattr(tree.__class__, "MUL") and tree.MUL():
            node = BinMulNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "MOD") and tree.MOD():
            node = BinModNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "DIS") and tree.DIS():
            node = BinDisNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "PLUS") and tree.PLUS():
            if tree.getChildCount() == 3:
                node = BinPlusNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))
            else:
                node = UnPlusNode(self.FindOp(tree.getChild(1)))

        elif hasattr(tree.__class__, "MIN") and tree.MIN():
            if tree.getChildCount() == 3:
                node = BinMinNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))
            else:
                node = UnMinNode(self.FindOp(tree.getChild(1)))

        elif hasattr(tree.__class__, "NOT") and tree.NOT():
            node = UnNotNode(self.FindOp(tree.getChild(1)))

        elif hasattr(tree.__class__, "AND") and tree.AND():
            node = BinAndNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "OR") and tree.OR():
            node = BinOrNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "LT") and tree.LT():
            node = BinLTNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "GT") and tree.GT():
            node = BinGTNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "EQ") and tree.EQ():
            node = BinEQNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "LTE") and tree.LTE():
            node = BinLTENode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "GTE") and tree.GTE():
            node = BinGTENode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "NE") and tree.NE():
            node = BinNENode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))

        elif hasattr(tree.__class__, "LBR") and tree.LBR() and tree.RBR():
            node = self.FindOp(tree.getChild(1))
        elif hasattr(tree.__class__, "SEMICOL") and tree.SEMICOL():
            node = self.FindOp(tree.getChild(0))
        elif hasattr(tree.__class__, "INT") and tree.INT():
            child = tree.INT()
            node = TermIntNode(int(child.getText()))
        elif hasattr(tree.__class__, "EOF") and tree.EOF():
            node = ProgramNode()
            for index in range(tree.getChildCount() - 1):
                node.addchild(self.FindOp(tree.getChild(index)))
        if not node:
            raise NameError("Unknown Node")
        return node

    def fold(self):
        self._root.fold()
