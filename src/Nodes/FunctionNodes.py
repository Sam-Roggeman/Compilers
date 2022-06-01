from Nodes.AbsNode import *
import SymbolTable


class FunctionNode(AbsNode):
    functionName: str

    def __init__(self, name):
        super().__init__()
        self.functionName = name
        self.argumentNode: ArgumentsNode = ArgumentsNode()

    def getName(self):
        return self.functionName

    def addArgument(self, child):
        self.argumentNode = child

    def getArguments(self):
        return self.argumentNode

    def getChildren(self):
        return [self.argumentNode]

    def fold(self):
        self.argumentNode = self.argumentNode.fold()
        return self

class FunctionCall(FunctionNode):
    def __init__(self,name):
        super().__init__(name)

    def toString(self):
        return "Functioncall" + " " +  self.functionName

class FunctionDefinition(FunctionNode):

    def __init__(self,name,type):
        super().__init__(name)
        self.functionbody: FunctionBody = None
        self.type = type
        self.symbol_table = SymbolTable.SymbolTable()

    def getSymbolTable(self):
        return self.symbol_table

    def setSymbolTabel(self, symboltable):
        self.symbol_table = symboltable

    def setFunctionbody(self,body):
        self.functionbody = body

    def checkParent(self,parent):
        self.parent = parent
        if self.argumentNode:
            self.argumentNode.checkParent(self)
        if self.functionbody:
            self.functionbody.checkParent(self)

    def toString(self):
        return self.type + " " + self.functionName
    def fold(self):
        super().fold()
        self.functionbody = self.functionbody.fold()
        return self

    def getChildren(self):
        children = []
        if self.functionbody:
            children.append(self.functionbody)
        if self.argumentNode:
            children.append(self.argumentNode)
        return children

class FunctionBody(AbsNode):
    body: list
    def __init__(self):
        super().__init__("FunctionBody")
        self.body = []

    def fold(self):
        for index in range(len(self.body)):
            self.body[index] = self.body[index].fold()
        return self

    def toString(self):
        return "functionbody"

    def checkParent(self,parent):
        self.parent = parent
        for c in self.body:
            c.setParent(self)

    def addBody(self,body):
        self.body.append(body)

    def getChildren(self):
        return self.body

class ReturnNode(AbsNode):
    def __init__(self):
        super().__init__("return")
        self.child = None

    def getChildren(self):
        return [self.child]

    def toString(self):
        return "return"

    def setChild(self, child, index: int = 0):
        self.child = child

class PrintfNode(FunctionNode):

    def __init__(self):
        super().__init__("printf")

    def toString(self):
        return "printf"

    def checkParent(self, parent=None):
        if parent:
            self.parent = parent
            for c in self.getChildren():
                c.checkParent(self)


class ArgumentsNode(AbsNode):

    def __init__(self):
        super().__init__("Arguments")
        self.children = []

    def addChild(self, child):
        child.rvalue = True
        self.children.append(child)

    def checkParent(self, parent=None):
        if parent:
            self.parent = parent
        for c in self.getChildren():
            c.setParent(self)

    def getChildren(self):
        return self.children

    def toString(self):
        return "Arguments"

    def fold(self):
        for index in range(len(self.children)):
            self.children[index] = self.children[index].fold()
        return self