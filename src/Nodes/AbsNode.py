from MetaData import *

class AbsNode:
    def setRvalue(self):
        self.rvalue = True

    def isRvalue(self):
        return self.rvalue

    def __str__(self):
        return self.toString()

    def setParent(self, parent):
        self.parent = parent

    def removeChild(self, index):
        pass

    def removeUnUsed(self):
        children = self.getChildren()
        for index in range(len(children) - 1, 0, -1):
            if children[index].checkUnUsed():
                self.removeChild(index)

    def checkUnUsed(self):
        return False

    def getLeftMostChild(self):
        children = self.getChildren()
        if len(children):
            return children[0].getLeftMostChild()
        else:
            return self

    def getLine(self):
        return self._metadata.getLine()

    def getColumn(self):
        return self._metadata.getColumn()

    def addMetaData(self, metadata: MetaData):
        self._metadata = metadata

    def getMetaData(self):
        return self._metadata

    def setChild(self, child, index: int = 0):
        pass

    def replaceConst(self):
        return False

    def __init__(self, parent=None):
        self.parent = parent
        self._metadata: MetaData
        self._lvalue = True
        self.rvalue = False
        self.symbol_table = None
        self.dead = False

    def getDead(self):
        return self.dead

    def setDead(self,dead):
        self.dead = dead
    def toString(self):
        return ""

    def fold(self):

        return self

    def getChildren(self):
        return []

    def toDot(self, dot):
        dot.node(str(id(self)), str(self))
        for child in self.getChildren():
            if child:
                child.toDot(dot)
                dot.edge(str(id(self)), str(id(child)))
        return dot

    def preOrderTraversal(self, string: str, oneline=True, indent=0):
        if oneline:
            string += self.toString() + ","
            for child in self.getChildren():
                string = child.preOrderTraversal(string, oneline)
        else:
            for i in range(0, indent):
                string += '\t'
            string += self.toString()
            string += '\n'
            for child in self.getChildren():
                string = child.preOrderTraversal(string, oneline, indent + 1)

        return string

    def isLvalue(self):
        return self._lvalue

    def solveTypes(self):
        children = self.getChildren()
        for index in range(len(children)):
            if children[index]:
                children[index].solveTypes()
