# Generated from ./src/g4_files/CGrammar2.g4 by ANTLR 4.9.3
from g4_files.CGrammar2Parser import CGrammar2Parser
from g4_files.CGrammar2Visitor import CGrammar2Visitor
from Nodes import *
from SymbolTable import *


# This class defines a complete generic visitor for a parse tree produced by CGrammar2Parser.

class CGrammar2VisitorImplementation(CGrammar2Visitor):
    _symbol_table: SymbolTable = SymbolTable()

    # Visit a parse tree produced by CGrammar2Parser#startRule.
    def visitStartRule(self, ctx: CGrammar2Parser.StartRuleContext):
        # print("visitStartRule")
        program_node = ProgramNode()
        for c in ctx.getChildren():
            astchild = self.visit(c)
            if astchild:
                program_node.addchild(astchild)

        return program_node

    # Visit a parse tree produced by CGrammar2Parser#expr.
    def visitExpr(self, ctx: CGrammar2Parser.ExprContext):
        # print("visitExpr")
        return self.visit(ctx.getChild(0))

    # Visit a parse tree produced by CGrammar2Parser#mathExpr.
    def visitMathExpr(self, ctx: CGrammar2Parser.MathExprContext):
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

    # Visit a parse tree produced by CGrammar2Parser#rvalue.
    def visitRvalue(self, ctx: CGrammar2Parser.RvalueContext):
        if ctx.variable():
            return self.visit(ctx.variable())
        elif ctx.mathExpr():
            return self.visit(ctx.mathExpr())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammar2Parser#binOp.
    # def visitBinOp(self, ctx: CGrammar2Parser.BinOpContext):

    # return self.visit(ctx.getChild(0))

    # Visit a parse tree produced by CGrammar2Parser#function.
    def visitFunction(self, ctx: CGrammar2Parser.FunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammar2Parser#declaration.
    def visitDeclaration(self, ctx: CGrammar2Parser.DeclarationContext):
        node = self.visit(ctx.types_specifier())
        name = ctx.variable().getText()
        node.setName(name)
        self._symbol_table.append(node)
        if ctx.CONST():
            node.makeConst()
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammar2Parser#declaration_assignment.
    def visitDeclaration_assignment(self, ctx: CGrammar2Parser.Declaration_assignmentContext):
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
        elif ctx.REF():
            node2 = RefNode()
            node2.setChild(self.visit(ctx.variable(1)))
        self._symbol_table.setValue(name,node2)
        assinmentNode = AssNode()
        assinmentNode.setChild(node1,0)
        assinmentNode.setChild(node2,1)
        return assinmentNode

    # Visit a parse tree produced by CGrammar2Parser#assignment.
    def visitAssignment(self, ctx: CGrammar2Parser.AssignmentContext):
        node1 = None
        node2 = None
        # todo error report
        name = ctx.variable()[0].getText()

        node1 = VariableNameNode()
        node1.setName(name=name)
        # Node2
        node2 = self.visit(ctx.rvalue())

        assinmentNode = AssNode()
        assinmentNode.setChild(node1,0)
        assinmentNode.setChild(node2,1)
        return assinmentNode

    # Visit a parse tree produced by CGrammar2Parser#reference.
    def visitReference(self, ctx: CGrammar2Parser.ReferenceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammar2Parser#poinervariable.
    def visitPointertype(self, ctx: CGrammar2Parser.PointertypeContext):
        # print("visitPoinervariable")
        if ctx.pointertype():
            a = PointerNode(self.visit(ctx.pointertype()))
            return a

        elif ctx.types_specifier():
            a = PointerNode(self.visit(ctx.types_specifier()))
            return a

    # Visit a parse tree produced by CGrammar2Parser#dereffedvariable.
    def visitDereffedvariable(self, ctx: CGrammar2Parser.DereffedvariableContext):
        # print("visitDereffedvariable")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammar2Parser#binOpPrio1.
    def visitBinOpPrio1(self, ctx: CGrammar2Parser.BinOpPrio1Context):
        # print("visitBinOpPrio1")
        if ctx.PLUS():
            return BinPlusNode()
        elif ctx.MIN():
            return BinMinNode()
        else:
            raise ValueError("Unknown Node")

    # Visit a parse tree produced by CGrammar2Parser#binOpPrio2.
    def visitBinOpPrio2(self, ctx: CGrammar2Parser.BinOpPrio2Context):
        # print("visitBinOpPrio2")
        if ctx.DIS():
            return BinDisNode()
        elif ctx.mul():
            return BinMulNode()
        elif ctx.MOD():
            return BinModNode()
        else:
            raise ValueError("Unknown Node")

    # Visit a parse tree produced by CGrammar2Parser#unOp.
    def visitUnOp(self, ctx: CGrammar2Parser.UnOpContext):
        # print("visitUnOp")
        if ctx.MIN():
            return UnMinNode()
        elif ctx.PLUS():
            return UnPlusNode()
        elif ctx.NOT():
            return UnNotNode()

    # Visit a parse tree produced by CGrammar2Parser#logOp.
    def visitLogOp(self, ctx: CGrammar2Parser.LogOpContext):
        # print("visitLogOp")
        if ctx.AND():
            return BinAndNode()
        elif ctx.OR():
            return BinOrNode()

    # Visit a parse tree produced by CGrammar2Parser#compOp.
    def visitCompOp(self, ctx: CGrammar2Parser.CompOpContext):
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

    # Visit a parse tree produced by CGrammar2Parser#mul.
    def visitMul(self, ctx: CGrammar2Parser.MulContext):
        # print("visitMul")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammar2Parser#deref.
    def visitDeref(self, ctx: CGrammar2Parser.DerefContext):
        # print("visitDeref")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammar2Parser#pointer.
    def visitPointer(self, ctx: CGrammar2Parser.PointerContext):
        # print("visitPointer")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammar2Parser#variable.
    def visitVariable(self, ctx: CGrammar2Parser.VariableContext):
        # print("visitVariable")
        node = VariableNameNode()
        node.setName(ctx.getText())
        return node

    # Visit a parse tree produced by CGrammar2Parser#types_specifier.
    def visitTypes_specifier(self, ctx: CGrammar2Parser.Types_specifierContext):
        # print("visitTypes_specifier")
        if ctx.CHARTYPE():
            return VariableCharNode()
        elif ctx.FLOATTYPE():
            return VariableFloatNode()
        elif ctx.INTTYPE():
            return VariableIntNode()

    # Visit a parse tree produced by CGrammar2Parser#literal.
    def visitLiteral(self, ctx: CGrammar2Parser.LiteralContext):
        # print("visitLiteral")
        if ctx.INTLit():
            return TermIntNode(int(ctx.INTLit().getText()))
        elif ctx.FLOATLit():
            return TermFloatNode(float(ctx.FLOATLit().getText()[:-1]))
        elif ctx.CHARLit():
            return TermCharNode(ctx.CHARLit().getText()[1:-1])

    # Visit a parse tree produced by CGrammar2Parser#const_qualifier.
    def visitConst_qualifier(self, ctx: CGrammar2Parser.Const_qualifierContext):
        # print("visitConst_qualifier")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammar2Parser#printf.
    def visitPrintf(self, ctx: CGrammar2Parser.PrintfContext):
        # print("visitPrintf")
        return self.visitChildren(ctx)

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

    def getSymbolTable(self):
        return self._symbol_table

del CGrammar2Parser
