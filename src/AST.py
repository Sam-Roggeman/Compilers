import graphviz
from SymbolTable import *


class AST:
    # todo parent

    _name = "output"
    _root: ProgramNode
    _working_node = None
    _last_entered_treenode = None
    _symbol_table: SymbolTable = SymbolTable()

    def __init__(self, tree, name=None):
        self._name = name
        try:
            self._root = self.FindOp(tree)
        except GeneralException as e:
            tree = self._last_entered_treenode
            e.setMetaData(metadata=MetaData(line=tree.start.line,start_character=tree.start.column))
            raise e

    def toDot(self, name: str, d_format="png"):
        dot = graphviz.Digraph(self._name, comment=self._name, strict=True)
        dot = self._root.toDot(dot)
        dot.render(filename="./output/" + self._name + "/" + name, format=d_format)
        return

    def FindType(self, name, tree):
        node = None
        if (self._symbol_table.isVar(name)):
           raise RedefinitionException(name)
        if hasattr(tree.__class__, "INTTYPE") and tree.INTTYPE():
            node = VariableIntNode(name)
        elif hasattr(tree.__class__, "FLOATTYPE") and tree.FLOATTYPE():
            node = VariableFloatNode(name)
        elif hasattr(tree.__class__, "CHARTYPE") and tree.CHARTYPE():
            node = VariableCharNode(name)
        elif hasattr(tree.__class__, "MUL") and tree.MUL():
            node = PointerNode(name, self.FindType("", tree.getChild(0)))

        if node.getName():
            self._symbol_table.append(node)

        if not node:
            print(type(tree))
            print(dir(tree))
            raise NameError("Unknown Node")
        return node

    def FindOp(self, tree):
        node = None
        self._last_entered_treenode = tree
        if hasattr(tree.__class__, "MUL") and tree.MUL():
            if tree.getChildCount() == 3:
                node = BinMulNode(self.FindOp(tree.getChild(0)), self.FindOp(tree.getChild(2)))
            elif tree.getChildCount() == 2:
                # node = self.findNode(name=tree.getChild(1).getText())
                self._working_node = self.FindOp(tree.expr()).deRef()
                node = self._working_node

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
        # elif hasattr(tree.__class__, "INTTYPE") and tree.INTTYPE():
        #     child = tree.INTTYPE()
        #     node = TermIntNode(int(child.getText()))

        elif hasattr(tree.__class__, "INT") and tree.INT():
            child = tree.INT()
            node = TermIntNode(int(child.getText()))

        elif hasattr(tree.__class__, "CHAR") and tree.CHAR():
            child = tree.CHAR()
            node = TermCharNode(child.getText()[1:-1])

        elif hasattr(tree.__class__, "FLOAT") and tree.FLOAT():
            child = tree.FLOAT()
            text = child.getText()[:-1]
            node = TermFloatNode(float(text))
        elif hasattr(tree.__class__, "mathExpr") and tree.mathExpr():
            node = self.FindOp(tree.getChild(0))
        elif hasattr(tree.__class__, "EOF") and tree.EOF():
            node = ProgramNode()
            for index in range(tree.getChildCount() - 1):
                node.addchild(self.FindOp(tree.getChild(index)))
        elif hasattr(tree.__class__, "type") and tree.type():
            node = self.FindType(tree.variable().getText(), tree.type())
            node.setChild(self.FindOp(tree.expr()))
            if hasattr(tree.__class__, "CONST") and tree.CONST():
                node.makeConst()

        elif hasattr(tree.__class__, "REF") and tree.REF():
            name = tree.getChild(tree.getChildCount() - 1).getText()
            node = self.findNode(name)
        elif hasattr(tree.__class__, "ASS") and tree.ASS():
            node = self.findNode(tree.variable().getText())
            node = node.copy()
            self._symbol_table.append(node)
            node.setChild(self.FindOp(tree.expr()))

        if not node:
            if hasattr(tree.__class__, "variable") and tree.variable():
                node = self.findNode(tree.variable().getText())

            elif hasattr(tree.__class__, "value") and tree.value():
                node = self.FindOp(tree.getChild(0))
            else:
                print(type(tree))
                print(dir(tree))
                raise NameError("Unknown Node")
        # print(dir(tree.start))
        node.addMetaData(metadata=MetaData(line=tree.start.line,start_character=tree.start.column))
        return node




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
        self._root = self._root.replaceConst()

    def optimize(self):
        self.toDot(name="start")
        self.replaceConst()
        self._symbol_table.reIndex()
        self.toDot(name="after_const")
        self.fold()
        self.toDot(name="end")
