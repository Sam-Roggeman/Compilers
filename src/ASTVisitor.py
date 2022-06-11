from Nodes.ArrayNodes import StringNode, ArrayNode, ArrayRefNode
from Nodes.Nodes import *
from SymbolTable import *


class AbsASTVisitor:
    _symbol_table: SymbolTable = None

    def __init__(self, ctx):
        self.visit(ctx)

    def visit(self, ctx: AbsNode):
        if isinstance(ctx, CodeblockNode):
            return self.visitCodeBlockNode(ctx)
        elif isinstance(ctx, TermNode):
            if isinstance(ctx, BreakNode):
                return self.visitBreakNode(ctx)
            elif isinstance(ctx, ContinueNode):
                return self.visitContinueNode(ctx)
            return self.visitTermNode(ctx)
        elif isinstance(ctx, UnOpNode):
            return self.visitUnOpNode(ctx)
        elif isinstance(ctx, AssNode):
            return self.visitAssNode(ctx)
        elif isinstance(ctx, ConditionNode):
            return self.visitConditionNode(ctx)
        elif isinstance(ctx, ArgumentsNode):
            return self.visitArgumentNode(ctx)
        elif isinstance(ctx, BinOpNode):
            if isinstance(ctx, BinPlusNode):
                return self.visitBinPlusNode(ctx)
            elif isinstance(ctx, BinOrNode):
                return self.visitBinOrNode(ctx)
            elif isinstance(ctx, BinAndNode):
                return self.visitBinAndNode(ctx)
            elif isinstance(ctx, BinNENode):
                return self.visitBinNENode(ctx)
            elif isinstance(ctx, BinEQNode):
                return self.visitBinEQNode(ctx)
            elif isinstance(ctx, BinDisNode):
                return self.visitBinDisNode(ctx)
            elif isinstance(ctx, BinModNode):
                return self.visitBinModNode(ctx)
            elif isinstance(ctx, BinMulNode):
                return self.visitBinMulNode(ctx)
            elif isinstance(ctx, BinMinNode):
                return self.visitBinMinNode(ctx)
            elif isinstance(ctx, BinGTENode):
                return self.visitBinGTENode(ctx)
            elif isinstance(ctx, BinGTNode):
                return self.visitBinGTNode(ctx)
            elif isinstance(ctx, BinLTNode):
                return self.visitBinLTNode(ctx)
            elif isinstance(ctx, BinLTENode):
                return self.visitBinLTENode(ctx)
        elif isinstance(ctx, VariableNode):
            if isinstance(ctx, VariableIntNode):
                return self.visitVariableIntNode(ctx)
            elif isinstance(ctx, VariableFloatNode):
                return self.visitVariableFloatNode(ctx)
            elif isinstance(ctx, VariableCharNode):
                return self.visitVariableCharNode(ctx)
            elif isinstance(ctx, PointerNode):
                # if isinstance(ctx, ArrayNode):
                if isinstance(ctx, StringNode):
                    return self.visitStringNode(ctx)
                    # return self.visitArrayNode(ctx)
                if isinstance(ctx, ArrayRefNode):
                    return self.visitArrayRefNode(ctx)

                return self.visitPointerNode(ctx)
        elif isinstance(ctx, VariableNameNode):
            return self.visitVariableNameNode(ctx)
        elif isinstance(ctx, FunctionNode):
            if isinstance(ctx, PrintfNode):
                return self.visitPrintfNode(ctx)
            elif isinstance(ctx, ScanfNode):
                return self.visitScanfNode(ctx)
            elif isinstance(ctx, FunctionDefinition):
                return self.visitFunctionDefinition(ctx)
            return self.visitFunctionNode(ctx)

        elif isinstance(ctx, ReturnNode):
            return self.visitReturnNode(ctx)
        elif isinstance(ctx, RefNode):
            return self.visitRefNode(ctx)
        elif isinstance(ctx, StatementNode):
            if isinstance(ctx, IfElseStatementNode):
                return self.visitIfElsestatementNode(ctx)
            elif isinstance(ctx, IfstatementNode):
                return self.visitIfstatementNode(ctx)
            elif isinstance(ctx, ElsestatementNode):
                return self.visitElsestatementNode(ctx)
            elif isinstance(ctx, WhilestatementNode):
                return self.visitWhilestatementNode(ctx)
            elif isinstance(ctx, ForstatementNode):
                return self.visitForstatementNode(ctx)
            else:
                return self.visitStatementNode(ctx)
        elif isinstance(ctx, FunctionBody):
            return self.visitFunctionBody(ctx)
        elif isinstance(ctx, DeRefNode):
            return self.visitDerefNode(ctx)

    def visitVariableFloatNode(self, ctx: VariableFloatNode):
        pass

    def visitVariableCharNode(self, ctx: VariableCharNode):
        pass

    def visitVariableIntNode(self, ctx: VariableIntNode):
        pass

    def visitChildren(self, ctx):
        for child in ctx.getChildren():
            self.visit(child)

    def visitCodeBlockNode(self, ctx: CodeblockNode):
        pass

    def visitTermNode(self, ctx: TermNode):
        pass

    def visitUnOpNode(self, ctx: UnOpNode):
        pass

    def visitBinOpNode(self, ctx: BinOpNode):
        pass

    def visitVariableNameNode(self, ctx: VariableNameNode):
        pass

    def visitVariableNode(self, ctx: VariableNode):
        pass

    def visitScanfNode(self, ctx: ScanfNode):
        pass

    def visitFunctionNode(self, ctx: FunctionNode):
        pass

    def visitPrintfNode(self, ctx: PrintfNode):
        pass

    def visitRefNode(self, ctx: RefNode):
        pass

    def visitAssNode(self, ctx: AssNode):
        pass

    def visitPointerNode(self, ctx: PointerNode):
        pass

    def visitArrayRefNode(self, ctx: ArrayRefNode):
        pass

    def visitBinLTENode(self, ctx: BinLTENode):
        pass

    def visitBinPlusNode(self, ctx: BinPlusNode):
        pass

    def visitBinAndNode(self, ctx: BinAndNode):
        pass

    def visitBinOrNode(self, ctx: BinOrNode):
        pass

    def visitBinEQNode(self, ctx: BinEQNode):
        pass

    def visitBinModNode(self, ctx: BinModNode):
        pass

    def visitBinDisNode(self, ctx: BinDisNode):
        pass

    def visitBinMinNode(self, ctx: BinMinNode):
        pass

    def visitBinGTNode(self, ctx: BinGTNode):
        pass

    def visitBinGTENode(self, ctx: BinGTENode):
        pass

    def visitBinNENode(self, ctx: BinNENode):
        pass

    def visitBinMulNode(self, ctx: BinMulNode):
        pass

    def visitBinLTNode(self, ctx: BinLTNode):
        pass

    def visitIfstatementNode(self, ctx: IfstatementNode):
        pass

    def visitElsestatementNode(self, ctx: ElsestatementNode):
        pass

    def visitWhilestatementNode(self, ctx: WhilestatementNode):
        pass

    def visitForstatementNode(self, ctx: ForstatementNode):
        pass

    def visitStatementNode(self, ctx: StatementNode):
        pass

    def visitArgumentNode(self, ctx: ArgumentsNode):
        pass

    def visitStringNode(self, ctx: StringNode):
        pass

    def visitFunctionDefinition(self, ctx: FunctionDefinition):
        pass

    def visitFunctionBody(self, ctx: FunctionBody):
        pass

    def visitIfElsestatementNode(self, ctx: IfElseStatementNode):
        pass

    def visitReturnNode(self, ctx: ReturnNode):
        pass

    def pushSymbolTable(self, symbol_table):
        symbol_table.parent = self._symbol_table
        self._symbol_table = symbol_table

    def popSymbolTable(self):
        self._symbol_table = self._symbol_table.parent

    def visitConditionNode(self, ctx):
        pass

    def visitBreakNode(self, ctx: BreakNode):
        pass

    def visitContinueNode(self, ctx: ContinueNode):
        pass

    def visitDerefNode(self, ctx: DeRefNode):
        pass


class ASTUsageVisitor(AbsASTVisitor):

    def __init__(self, ctx):
        super().__init__(ctx)

    def default(self, ctx):
        for index in range(len(ctx.getChildren())):
            self.visit(ctx.getChildren()[index])

    def visitVariableNameNode(self, ctx):
        self.default(ctx)

    def visitVariableNode(self, ctx: VariableNode):

        if ctx.isRvalue():
            return self._symbol_table.foundRHS(ctx.getName())
        self._symbol_table.foundLHS(ctx.getName())

    def visitVariableFloatNode(self, ctx):
        self.visitVariableNode(ctx)

    def visitVariableCharNode(self, ctx):
        self.visitVariableNode(ctx)

    def visitVariableIntNode(self, ctx):
        self.visitVariableNode(ctx)

    def visitChildren(self, ctx):
        for child in ctx.getChildren():
            self.visit(child)

    def visitCodeBlockNode(self, ctx):
        self.pushSymbolTable(ctx.getSymbolTable())
        self.default(ctx)
        self.popSymbolTable()

    def visitTermNode(self, ctx):
        self.default(ctx)

    def visitUnOpNode(self, ctx):
        self.default(ctx)

    def visitBinOpNode(self, ctx):
        self.default(ctx)

    def visitFunctionNode(self, ctx):
        self.default(ctx)

    def visitPrintfNode(self, ctx):
        self.default(ctx)

    def visitRefNode(self, ctx):
        self.default(ctx)

    def visitAssNode(self, ctx):
        self.default(ctx)
    def visitPointerNode(self, ctx):
        self.visitVariableNode(ctx)

    def visitBinLTENode(self, ctx):
        self.default(ctx)

    def visitBinPlusNode(self, ctx):
        self.default(ctx)

    def visitBinAndNode(self, ctx):
        self.default(ctx)

    def visitBinOrNode(self, ctx):
        self.default(ctx)

    def visitBinEQNode(self, ctx):
        self.default(ctx)

    def visitBinModNode(self, ctx):
        self.default(ctx)

    def visitBinDisNode(self, ctx):
        self.default(ctx)

    def visitBinMinNode(self, ctx):
        self.default(ctx)

    def visitBinGTNode(self, ctx):
        self.default(ctx)

    def visitBinGTENode(self, ctx):
        self.default(ctx)

    def visitBinNENode(self, ctx):
        self.default(ctx)

    def visitBinMulNode(self, ctx):
        self.default(ctx)

    def visitBinLTNode(self, ctx):
        self.default(ctx)

    def visitIfstatementNode(self, ctx):
        self.pushSymbolTable(ctx.getSymbolTable())
        self.default(ctx)
        self.popSymbolTable()

    def visitElsestatementNode(self, ctx):
        self.pushSymbolTable(ctx.getSymbolTable())
        self.default(ctx)
        self.popSymbolTable()

    def visitWhilestatementNode(self, ctx):
        self.pushSymbolTable(ctx.getSymbolTable())
        self.default(ctx)
        self.popSymbolTable()

    def visitForstatementNode(self, ctx):
        self.pushSymbolTable(ctx.getSymbolTable())
        self.default(ctx)
        self.popSymbolTable()

    def visitStatementNode(self, ctx):
        self.pushSymbolTable(ctx.getSymbolTable())
        self.default(ctx)
        self.popSymbolTable()


class ASTConstVisitor(AbsASTVisitor):

    def default(self, ctx: AbsNode):
        for index in range(len(ctx.getChildren())):
            ctx.setChild(self.visit(ctx.getChildren()[index]), index)

        return ctx

    def visitCodeBlockNode(self, ctx: CodeblockNode):
        return self.default(ctx)

    def visitTermNode(self, ctx: TermNode):
        return self.default(ctx)

    def visitUnOpNode(self, ctx: UnOpNode):
        return self.default(ctx)

    def visitBinOpNode(self, ctx: BinOpNode):
        return self.default(ctx)

    def visitVariableNameNode(self, ctx: VariableNameNode):
        node = self._symbol_table.getVar(ctx.getName())
        if ctx.isRvalue() and not ctx.isReferenced() and node.isConst():
            return copy.deepcopy(self._symbol_table.getValue(ctx.getName()))
        else:
            return ctx

    def visitVariableNode(self, ctx: VariableNode):
        node = self._symbol_table.getVar(ctx.getName())
        if ctx.isRvalue() and not ctx.isReferenced() and node.isConst():
            return copy.deepcopy(self._symbol_table.getValue(ctx.getName()))
        else:
            return ctx

    def visitVariableFloatNode(self, ctx: VariableFloatNode):
        return self.visitVariableNode(ctx)

    def visitVariableCharNode(self, ctx: VariableCharNode):
        return self.visitVariableNode(ctx)

    def visitVariableIntNode(self, ctx: VariableIntNode):
        return self.visitVariableNode(ctx)

    def visitFunctionNode(self, ctx: FunctionNode):
        return self.default(ctx)

    def visitPrintfNode(self, ctx: PrintfNode):
        return self.default(ctx)

    def visitRefNode(self, ctx: RefNode):
        return self.default(ctx)

    def visitAssNode(self, ctx: AssNode):
        return self.default(ctx)

    def visitPointerNode(self, ctx: PointerNode):
        return self.default(ctx)

    def visitBinLTENode(self, ctx: BinLTENode):
        return self.visitBinOpNode(ctx)

    def visitBinPlusNode(self, ctx: BinPlusNode):
        return self.visitBinOpNode(ctx)

    def visitBinAndNode(self, ctx: BinAndNode):
        return self.visitBinOpNode(ctx)

    def visitBinOrNode(self, ctx: BinOrNode):
        return self.visitBinOpNode(ctx)

    def visitBinEQNode(self, ctx: BinEQNode):
        return self.visitBinOpNode(ctx)

    def visitBinModNode(self, ctx: BinModNode):
        return self.visitBinOpNode(ctx)

    def visitBinDisNode(self, ctx: BinDisNode):
        return self.visitBinOpNode(ctx)

    def visitBinMinNode(self, ctx: BinMinNode):
        return self.visitBinOpNode(ctx)

    def visitBinGTNode(self, ctx: BinGTNode):
        return self.visitBinOpNode(ctx)

    def visitBinGTENode(self, ctx: BinGTENode):
        return self.visitBinOpNode(ctx)

    def visitBinNENode(self, ctx: BinNENode):
        return self.visitBinOpNode(ctx)

    def visitBinMulNode(self, ctx: BinMulNode):
        return self.visitBinOpNode(ctx)

    def visitBinLTNode(self, ctx: BinLTNode):
        return self.visitBinOpNode(ctx)


class RemoveUnUsed(AbsASTVisitor):
    def visitCodeBlockNode(self, ctx: CodeblockNode):
        for index in range(len(ctx.getChildren()) - 1, -1, -1):
            if self.visit(ctx.getChildren()[index]):
                ctx.children.pop(index)

    def visitTermNode(self, ctx: TermNode):

        return False

    def visitUnOpNode(self, ctx: UnOpNode):
        return False

    def visitBinOpNode(self, ctx: BinOpNode):
        return False

    def visitVariableNameNode(self, ctx: VariableNameNode):
        node = self._symbol_table.getVar(ctx.getName())
        if node:
            return node.isUnUsed()

    def visitVariableFloatNode(self, ctx: VariableFloatNode):
        return self.visitVariableNode(ctx)

    def visitVariableCharNode(self, ctx: VariableCharNode):
        return self.visitVariableNode(ctx)

    def visitVariableIntNode(self, ctx: VariableIntNode):
        return self.visitVariableNode(ctx)

    #     else exception todo

    def visitVariableNode(self, ctx: VariableNode):
        return ctx.isUnUsed()

    def visitFunctionNode(self, ctx: FunctionNode):
        return False

    def visitPrintfNode(self, ctx: PrintfNode):
        return False

    def visitRefNode(self, ctx: RefNode):
        return False

    def visitAssNode(self, ctx: AssNode):
        return self.visit(ctx.getChildren()[0])

    def visitPointerNode(self, ctx: PointerNode):
        return False

    def visitBinLTENode(self, ctx: BinLTENode):
        return self.visitBinOpNode(ctx)

    def visitBinPlusNode(self, ctx: BinPlusNode):
        return self.visitBinOpNode(ctx)

    def visitBinAndNode(self, ctx: BinAndNode):
        return self.visitBinOpNode(ctx)

    def visitBinOrNode(self, ctx: BinOrNode):
        return self.visitBinOpNode(ctx)

    def visitBinEQNode(self, ctx: BinEQNode):
        return self.visitBinOpNode(ctx)

    def visitBinModNode(self, ctx: BinModNode):
        return self.visitBinOpNode(ctx)

    def visitBinDisNode(self, ctx: BinDisNode):
        return self.visitBinOpNode(ctx)

    def visitBinMinNode(self, ctx: BinMinNode):
        return self.visitBinOpNode(ctx)

    def visitBinGTNode(self, ctx: BinGTNode):
        return self.visitBinOpNode(ctx)

    def visitBinGTENode(self, ctx: BinGTENode):
        return self.visitBinOpNode(ctx)

    def visitBinNENode(self, ctx: BinNENode):
        return self.visitBinOpNode(ctx)

    def visitBinMulNode(self, ctx: BinMulNode):
        return self.visitBinOpNode(ctx)

    def visitBinLTNode(self, ctx: BinLTNode):
        return self.visitBinOpNode(ctx)
