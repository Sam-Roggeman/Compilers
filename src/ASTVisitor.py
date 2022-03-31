from SymbolTable import *
from Nodes import *


class AbsASTVisitor:
    _symbol_table: SymbolTable

    def __init__(self, ctx, symbol_table):
        self._symbol_table = symbol_table
        self.visit(ctx)

    def visit(self, ctx):
        if isinstance(ctx, ProgramNode):
            return self.visitProgramNode(ctx)
        elif isinstance(ctx, TermNode):
            return self.visitTermNode(ctx)
        elif isinstance(ctx, UnOpNode):
            return self.visitUnOpNode(ctx)
        elif isinstance(ctx, AssNode):
            return self.visitAssNode(ctx)
        elif isinstance(ctx, BinOpNode):
            return self.visitBinOpNode(ctx)
        elif isinstance(ctx, VariableNode):
            return self.visitVariableNode(ctx)
        elif isinstance(ctx, VariableNameNode):
            return self.visitVariableNameNode(ctx)
        elif isinstance(ctx, FunctionNode):
            return self.visitFunctionNode(ctx)
        elif isinstance(ctx, PrintfNode):
            return self.visitPrintfNode(ctx)
        elif isinstance(ctx, PointerNode):
            return self.visitPointerNode(ctx)

        elif isinstance(ctx, RefNode):
            return self.visitRefNode(ctx)

    def visitChildren(self, ctx):
        for child in ctx.getChildren():
            self.visit(child)

    def visitProgramNode(self, ctx):
        print("hi")
        pass

    def visitTermNode(self, ctx):
        pass

    def visitUnOpNode(self, ctx):
        pass

    def visitBinOpNode(self, ctx):
        pass

    def visitVariableNameNode(self, ctx):
        pass

    def visitVariableNode(self, ctx):
        pass

    def visitFunctionNode(self, ctx):
        pass

    def visitPrintfNode(self, ctx):
        pass

    def visitRefNode(self, ctx):
        pass

    def visitAssNode(self, ctx):
        pass

    def visitPointerNode(self, ctx):
        pass


class ASTConstVisitor(AbsASTVisitor):

    def default(self,ctx):
        for index in range(len(ctx.getChildren())):
            ctx.setChild(self.visit(ctx.getChildren()[index]), index)

        return ctx

    def visitProgramNode(self, ctx):
        return self.default(ctx)

    def visitTermNode(self, ctx):
        return self.default(ctx)

    def visitUnOpNode(self, ctx):
        return self.default(ctx)

    def visitBinOpNode(self, ctx):
        return self.default(ctx)

    def visitVariableNameNode(self, ctx):
        if self._symbol_table.getConst(ctx.getName()):
            return self._symbol_table.getValue(ctx.getName())
        else:
            return self

    def visitVariableNode(self, ctx):
        if ctx.isConst():
            return self._symbol_table.getValue(ctx.getName())
        else:
            return self

    def visitFunctionNode(self, ctx):
        return self.default(ctx)

    def visitPrintfNode(self, ctx):
        return self.default(ctx)

    def visitRefNode(self, ctx):
        return self.default(ctx)

    def visitAssNode(self, ctx):
        return self.default(ctx)

    def visitPointerNode(self, ctx):
        return self.default(ctx)


class removeUnUsed(AbsASTVisitor):
    def visitProgramNode(self, ctx):
        for index in range(len(ctx.getChildren()) - 1, -1, -1):
            if self.visit(ctx.getChildren()[index]):
                ctx.children.pop(index)

    def visitTermNode(self, ctx):

        return False

    def visitUnOpNode(self, ctx):
        return False

    def visitBinOpNode(self, ctx):
        return False

    def visitVariableNameNode(self, ctx: VariableNameNode):
        node = self._symbol_table.getVar(ctx.getName())
        if node:
            return node.isUnUsed()

    #     else exception todo

    def visitVariableNode(self, ctx):
        return ctx.isUnUsed()

    def visitFunctionNode(self, ctx):
        return False

    def visitPrintfNode(self, ctx):
        return False

    def visitRefNode(self, ctx):
        return False

    def visitAssNode(self, ctx):
        return self.visit(ctx.getChildren()[0])

    def visitPointerNode(self, ctx):
        return False
