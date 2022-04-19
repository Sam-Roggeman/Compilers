# Generated from ./src/g4_files/CGrammar.g4 by ANTLR 4.9.3
from g4_files.CGrammarParser import CGrammarParser
from g4_files.CGrammarVisitor import CGrammarVisitor
from Nodes import *
from SymbolTable import *


# This class defines a complete generic visitor for a parse tree produced by CGrammarParser.

class CGrammarVisitorImplementation(CGrammarVisitor):
    _symbol_table: SymbolTable = SymbolTable()

    # Visit a parse tree produced by CGrammarParser#startRule.
    def visitStartRule(self, ctx: CGrammarParser.StartRuleContext):
        # print("visitStartRule")
        return self.visit(ctx.file())

    # Visit a parse tree produced by CGrammarParser#expr.
    def visitExpr(self, ctx: CGrammarParser.ExprContext):
        # print("visitExpr")
        return self.visit(ctx.getChild(0))

    # Visit a parse tree produced by CGrammarParser#mathExpr.
    def visitMathExpr(self, ctx: CGrammarParser.MathExprContext):
        # print("visitMathExpr")
        count = ctx.getChildCount()
        if count == 1:
            # literal or variable
            return self.visit(ctx.getChild(0))
        elif count == 2:
            if ctx.unOp():
                op = self.visit(ctx.unOp())
                expr = self.visit(ctx.mathExpr()[0])
                op.setChild(expr)
                return op

        elif count == 3:
            if ctx.LBR() and ctx.RBR() and ctx.mathExpr():
                # (mathexpr)
                return self.visit(ctx.mathExpr()[0])
            # a bin-operator b
            children = ctx.mathExpr()
            # a
            child1 = self.visit(children[0])
            # b
            child2 = self.visit(children[1])
            # bin-operator
            operator_node: BinOpNode = None
            if ctx.binOpPrio1():
                operator_node = self.visit(ctx.binOpPrio1())

            elif ctx.binOpPrio2():
                operator_node = self.visit(ctx.binOpPrio2())
            elif ctx.compOp():
                operator_node = self.visit(ctx.compOp())
            elif ctx.logOp():
                operator_node = self.visit(ctx.logOp())
            operator_node.setChildren(child1, child2)
            return operator_node
        else:
            raise ValueError("Unknown Node")

    # Visit a parse tree produced by CGrammarParser#rvalue.
    def visitRvalue(self, ctx: CGrammarParser.RvalueContext):
        if ctx.variable():
            return self.visit(ctx.variable())
        elif ctx.mathExpr():
            return self.visit(ctx.mathExpr())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#binOp.
    # def visitBinOp(self, ctx: CGrammarParser.BinOpContext):

    # return self.visit(ctx.getChild(0))

    # Visit a parse tree produced by CGrammarParser#function.
    def visitFunction(self, ctx: CGrammarParser.FunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#declaration.
    def visitDeclaration(self, ctx: CGrammarParser.DeclarationContext):
        node = self.visit(ctx.types_specifier())
        name = ctx.variable().getText()
        node.setName(name)
        self._symbol_table.append(node)
        if ctx.CONST():
            node.makeConst()
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#declaration_assignment.
    def visitDeclaration_assignment(self, ctx: CGrammarParser.Declaration_assignmentContext):
        node1 = None
        node2 = None

        # Node1
        if ctx.types_specifier():
            node1 = self.visit(ctx.types_specifier())
        elif ctx.pointertype():
            node1 = self.visit(ctx.pointertype())

        name = ctx.variable()[0].getText()
        node1.setName(name)
        self._symbol_table.append(node1)
        if ctx.CONST():
            node1.makeConst()

        # Node2
        if ctx.rvalue():
            node2 = self.visit(ctx.rvalue())
            for c in node2.getChildren():
                c.setRvalue()
            node2.setRvalue()
        elif ctx.REF():
            node2 = RefNode()
            child = self.visit(ctx.variable(1))
            child.setReferenced()
            child.setRvalue()
            node2.setChild(child)
            node2.setRvalue()

        self._symbol_table.setValue(name,node2)
        assinmentNode = AssNode()
        assinmentNode.setChild(node1,0)
        assinmentNode.setChild(node2,1)
        return assinmentNode

    # Visit a parse tree produced by CGrammarParser#assignment.
    def visitAssignment(self, ctx: CGrammarParser.AssignmentContext):
        node1 = None
        node2 = None
        # todo error report
        name = ctx.variable()[0].getText()
        node1 = copy.deepcopy(self._symbol_table.getVar(varname=ctx.getText()))
        # Node2
        node2 = self.visit(ctx.rvalue())
        self._symbol_table.setValue(name,node2)
        assinmentNode = AssNode()
        assinmentNode.setChild(node1,0)
        assinmentNode.setChild(node2,1)
        return assinmentNode

    # Visit a parse tree produced by CGrammarParser#reference.
    def visitReference(self, ctx: CGrammarParser.ReferenceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#poinervariable.
    def visitPointertype(self, ctx: CGrammarParser.PointertypeContext):
        # print("visitPoinervariable")
        if ctx.pointertype():
            a = PointerNode(self.visit(ctx.pointertype()))
            return a

        elif ctx.types_specifier():
            a = PointerNode(self.visit(ctx.types_specifier()))
            return a

    # Visit a parse tree produced by CGrammarParser#dereffedvariable.
    def visitDereffedvariable(self, ctx: CGrammarParser.DereffedvariableContext):
        # print("visitDereffedvariable")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#binOpPrio1.
    def visitBinOpPrio1(self, ctx: CGrammarParser.BinOpPrio1Context):
        # print("visitBinOpPrio1")
        if ctx.PLUS():
            return BinPlusNode()
        elif ctx.MIN():
            return BinMinNode()
        else:
            raise ValueError("Unknown Node")

    # Visit a parse tree produced by CGrammarParser#binOpPrio2.
    def visitBinOpPrio2(self, ctx: CGrammarParser.BinOpPrio2Context):
        # print("visitBinOpPrio2")
        if ctx.DIS():
            return BinDisNode()
        elif ctx.mul():
            return BinMulNode()
        elif ctx.MOD():
            return BinModNode()
        else:
            raise ValueError("Unknown Node")

    # Visit a parse tree produced by CGrammarParser#unOp.
    def visitUnOp(self, ctx: CGrammarParser.UnOpContext):
        # print("visitUnOp")
        if ctx.MIN():
            return UnMinNode()
        elif ctx.PLUS():
            return UnPlusNode()
        elif ctx.NOT():
            return UnNotNode()

    # Visit a parse tree produced by CGrammarParser#logOp.
    def visitLogOp(self, ctx: CGrammarParser.LogOpContext):
        # print("visitLogOp")
        if ctx.AND():
            return BinAndNode()
        elif ctx.OR():
            return BinOrNode()

    # Visit a parse tree produced by CGrammarParser#compOp.
    def visitCompOp(self, ctx: CGrammarParser.CompOpContext):
        # print("visitCompOp")

        if ctx.EQ():
            return BinEQNode()
        elif ctx.GTE():
            return BinGTENode()
        elif ctx.GT():
            return BinGTNode()
        elif ctx.LT():
            return BinLTNode()
        elif ctx.LTE():
            return BinLTENode()
        elif ctx.NE():
            return BinNENode()

    # Visit a parse tree produced by CGrammarParser#mul.
    def visitMul(self, ctx: CGrammarParser.MulContext):
        # print("visitMul")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#deref.
    def visitDeref(self, ctx: CGrammarParser.DerefContext):
        # print("visitDeref")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#pointer.
    def visitPointer(self, ctx: CGrammarParser.PointerContext):
        # print("visitPointer")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#variable.
    def visitVariable(self, ctx: CGrammarParser.VariableContext):
        # print("visitVariable")
        node = copy.deepcopy(self._symbol_table.getVar(varname=ctx.getText()))

        return node

    # Visit a parse tree produced by CGrammarParser#types_specifier.
    def visitTypes_specifier(self, ctx: CGrammarParser.Types_specifierContext):
        # print("visitTypes_specifier")
        if ctx.CHARTYPE():
            return VariableCharNode()
        elif ctx.FLOATTYPE():
            return VariableFloatNode()
        elif ctx.INTTYPE():
            return VariableIntNode()

    # Visit a parse tree produced by CGrammarParser#literal.
    def visitLiteral(self, ctx: CGrammarParser.LiteralContext):
        # print("visitLiteral")
        if ctx.INTLit():
            return TermIntNode(int(ctx.INTLit().getText()))
        elif ctx.FLOATLit():
            return TermFloatNode(float(ctx.FLOATLit().getText()[:-1]))
        elif ctx.CHARLit():
            return TermCharNode(ctx.CHARLit().getText()[1:-1])

    # Visit a parse tree produced by CGrammarParser#const_qualifier.
    def visitConst_qualifier(self, ctx: CGrammarParser.Const_qualifierContext):
        # print("visitConst_qualifier")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#printf.
    def visitPrintf(self, ctx: CGrammarParser.PrintfContext):
        # print("visitPrintf")
        return self.visitChildren(ctx)

    def visitFile(self, ctx:CGrammarParser.FileContext):
        node1 = CodeblockNode()
        for c in ctx.getChildren():
            print(c.getText())
            astchild = self.visit(c)
            if astchild:
                node1.addchild(astchild)

        return node1

    def visitStatement(self, ctx:CGrammarParser.StatementContext):
        node1 = StatementNode()
        for c in ctx.getChildren():
            astchild = self.visit(c)
            if astchild:
                node1.addChild(astchild)

        return node1

    def visitIfstatement(self, ctx:CGrammarParser.IfstatementContext):
        condition = ConditionNode()
        child = self.visit(ctx.expr())
        condition.addChild(child)
        codeblock = self.visit(ctx.file())
        node = IfstatementNode()
        node.setCondition(condition)
        node.setBlock(codeblock)
        return node

    def visitElsestatement(self, ctx:CGrammarParser.ElsestatementContext):
        codeblock = self.visit(ctx.file())
        node = ElsestatementNode()
        node.setBlock(codeblock)
        return node

    def visitWhilestatement(self, ctx:CGrammarParser.WhilestatementContext):
        condition = ConditionNode()
        child = self.visit(ctx.expr())
        condition.addChild(child)
        codeblock = self.visit(ctx.file())
        node = WhilestatementNode()
        node.setCondition(condition)
        node.setBlock(codeblock)
        return node

    def visitForstatement(self, ctx:CGrammarParser.ForstatementContext):
        condition = ConditionNode()
        expressions = ctx.expr()
        for c in range(len(expressions)):
            expr = self.visit(ctx.expr(c))
            condition.addChild(expr)
        codeblock = self.visit(ctx.file())
        node = ForstatementNode()
        node.setCondition(condition)
        node.setBlock(codeblock)
        return node

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

    def getSymbolTable(self):
        return self._symbol_table


del CGrammarParser
