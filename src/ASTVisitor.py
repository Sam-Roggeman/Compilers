from Nodes import *
from SymbolTable import *


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
            if isinstance(ctx, BinPlusNode):
                return self.visitBinPlusNode(ctx)
            elif isinstance(ctx,BinOrNode):
                return self.visitBinOrNode(ctx)
            elif isinstance(ctx,BinAndNode):
                return self.visitBinAndNode(ctx)
            elif isinstance(ctx,BinNENode):
                return self.visitBinNENode(ctx)
            elif isinstance(ctx,BinEQNode):
                return self.visitBinEQNode(ctx)
            elif isinstance(ctx,BinDisNode):
                return self.visitBinDisNode(ctx)
            elif isinstance(ctx,BinModNode):
                return self.visitBinModNode(ctx)
            elif isinstance(ctx,BinMulNode):
                return self.visitBinMulNode(ctx)
            elif isinstance(ctx,BinMinNode):
                return self.visitBinMinNode(ctx)
            elif isinstance(ctx,BinGTENode):
                return self.visitBinGTENode(ctx)
            elif isinstance(ctx,BinGTNode):
                return self.visitBinGTNode(ctx)
            elif isinstance(ctx,BinLTNode):
                return self.visitBinLTNode(ctx)
            elif isinstance(ctx,BinLTENode):
                return self.visitBinLTENode(ctx)
        elif isinstance(ctx, VariableNode):
            if isinstance(ctx, VariableIntNode):
                return self.visitVariableIntNode(ctx)
            elif isinstance(ctx, VariableFloatNode):
                return self.visitVariableFloatNode(ctx)
            elif isinstance(ctx, VariableCharNode):
                return self.visitVariableCharNode(ctx)
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

    def visitVariableFloatNode(self, ctx):
        pass

    def visitVariableCharNode(self, ctx):
        pass

    def visitVariableIntNode(self, ctx):
        pass

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

    def visitBinLTENode(self, ctx):
        pass

    def visitBinPlusNode(self, ctx):
        pass

    def visitBinAndNode(self, ctx):
        pass

    def visitBinOrNode(self, ctx):
        pass

    def visitBinEQNode(self, ctx):
        pass

    def visitBinModNode(self, ctx):
        pass

    def visitBinDisNode(self, ctx):
        pass

    def visitBinMinNode(self, ctx):
        pass

    def visitBinGTNode(self, ctx):
        pass

    def visitBinGTENode(self, ctx):
        pass

    def visitBinNENode(self, ctx):
        pass

    def visitBinMulNode(self, ctx):
        pass

    def visitBinLTNode(self, ctx):
        pass


class ASTConstVisitor(AbsASTVisitor):

    def default(self, ctx):
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
        node = self._symbol_table.getVar(ctx.getName())
        if ctx.isRvalue() and not ctx.isReferenced() and node.isConst():
            return copy.deepcopy(self._symbol_table.getValue(ctx.getName()))
        else:
            return ctx

    def visitVariableNode(self, ctx):
        node = self._symbol_table.getVar(ctx.getName())
        if ctx.isRvalue() and ctx.isReferenced() == False and node.isConst():
            return copy.deepcopy(self._symbol_table.getValue(ctx.getName()))
        else:
            return ctx

    def visitVariableFloatNode(self, ctx):
        return self.visitVariableNode(ctx)

    def visitVariableCharNode(self, ctx):
        return self.visitVariableNode(ctx)

    def visitVariableIntNode(self, ctx):
        return self.visitVariableNode(ctx)

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
    def visitBinLTENode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinPlusNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinAndNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinOrNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinEQNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinModNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinDisNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinMinNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinGTNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinGTENode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinNENode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinMulNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinLTNode(self, ctx):
        return self.visitBinOpNode(ctx)

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

    def visitVariableFloatNode(self, ctx):
        return self.visitVariableNode(ctx)

    def visitVariableCharNode(self, ctx):
        return self.visitVariableNode(ctx)

    def visitVariableIntNode(self, ctx):
        return self.visitVariableNode(ctx)

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
    def visitBinLTENode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinPlusNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinAndNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinOrNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinEQNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinModNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinDisNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinMinNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinGTNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinGTENode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinNENode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinMulNode(self, ctx):
        return self.visitBinOpNode(ctx)

    def visitBinLTNode(self, ctx):
        return self.visitBinOpNode(ctx)