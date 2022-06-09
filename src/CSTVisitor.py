# Generated from ./src/g4_files/CGrammar.g4 by ANTLR 4.9.3
from Nodes.Nodes import *
from SymbolTable import *
from g4_files.CGrammarParser import CGrammarParser
from g4_files.CGrammarVisitor import CGrammarVisitor


# This class defines a complete generic visitor for a parse tree produced by CGrammarParser.

class CGrammarVisitorImplementation(CGrammarVisitor):
    def __init__(self):
        self.symbol_table = None
        self.visitedmain = False
        self.counter = 0

    def addMetaData(self, meta, node):
        node.addMetaData(MetaData(line=meta.start.line, start_character=meta.start.column, end_line=meta.stop.line,
                                  end_character=meta.stop.column))

    def visitDecr(self, ctx: CGrammarParser.DecrContext):
        return BinMinNode()

    def visitIncr(self, ctx: CGrammarParser.IncrContext):
        return BinPlusNode()

    def visitIncr_decr(self, ctx: CGrammarParser.Incr_decrContext):
        return self.visit(ctx.children[0])

    # Visit a parse tree produced by CGrammarParser#startRule.
    def visitStartRule(self, ctx: CGrammarParser.StartRuleContext):
        # print("visitStartRule")
        tree = self.visit(ctx.file())
        if not self.getVisitedMain():
            raise mainNotFound("")
        return tree

    # Visit a parse tree produced by CGrammarParser#expr.
    def visitExpr(self, ctx: CGrammarParser.ExprContext):
        # print("visitExpr")
        return self.visit(ctx.getChild(0))

    # Visit a parse tree produced by CGrammarParser#mathExpr.
    def visitMathExpr(self, ctx: CGrammarParser.MathExprContext):
        # print("visitMathExpr")
        count = ctx.getChildCount()
        # if ctx.ASS() and not ctx.getChild(0).variable():
        #     raise RValueException()
        if count == 1:
            # literal or variable
            return self.visit(ctx.getChild(0))
        elif count == 2:
            if ctx.unOp():
                op = self.visit(ctx.unOp())
                expr = self.visit(ctx.mathExpr()[0])
                op.setChild(expr)
                return op
            elif ctx.incr_decr():
                child1 = self.visit(ctx.mathExpr()[0])
                child2 = TermIntNode(1)
                operator_node = self.visit(ctx.incr_decr())
                operator_node.setChildren(child1, child2)
                ass = AssNode()
                ass.rhs = operator_node
                ass.lhs = child1

                return ass


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
            if ctx.binOpPrio1() or ctx.binOpPrio2():
                operatorChildren = operator_node.getChildren()
                if type(operatorChildren[0]) == PointerNode and type(operatorChildren[1]) == PointerNode:
                    raise pointerOperationError(operator_node.toString())
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
        self.symbol_table.append(node)
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
        self.symbol_table.append(node1)
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
        elif ctx.functioncall():
            node2 = self.visit(ctx.functioncall())

        self.symbol_table.setValue(name, node2)
        if not node2:
            self.addMetaData(ctx, node1)
            return node1
        assignmentNode = AssNode()
        assignmentNode.setChild(node1, 0)
        assignmentNode.setChild(node2, 1)
        self.addMetaData(ctx, assignmentNode)
        return assignmentNode

    # Visit a parse tree produced by CGrammarParser#assignment.
    def visitAssignment(self, ctx: CGrammarParser.AssignmentContext):
        node1 = None
        node2 = None
        name: str
        # todo error report
        if ctx.variable():
            name = ctx.variable()[0].getText()
        elif ctx.dereffedvariable():
            # name of pointer
            name = ctx.dereffedvariable().variable().getText()
            # the adress that is pointed to
            ref = self.symbol_table.getTableEntry(name).value
            # the variable under the adress
            name = ref.child.getName()

        node1 = copy.deepcopy(self.symbol_table.getVar(varname=name))
        if self.symbol_table.getConst(name):
            raise ConstException(varname=name)
        # Node2
        node2 = self.visit(ctx.rvalue())
        self.symbol_table.setValue(name, node2)
        assinmentNode = AssNode()
        assinmentNode.setChild(node1, 0)
        assinmentNode.setChild(node2, 1)
        self.addMetaData(ctx, assinmentNode)
        return assinmentNode

    # Visit a parse tree produced by CGrammarParser#reference.
    def visitReference(self, ctx: CGrammarParser.ReferenceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#poinervariable.
    def visitPointertype(self, ctx: CGrammarParser.PointertypeContext):
        # print("visitPoinervariable")
        if ctx.pointertype():
            a = PointerNode(self.visit(ctx.pointertype()))
            self.addMetaData(ctx, a)
            return a

        elif ctx.types_specifier():
            a = PointerNode(self.visit(ctx.types_specifier()))
            self.addMetaData(ctx, a)
            return a

    # Visit a parse tree produced by CGrammarParser#dereffedvariable.
    def visitDereffedvariable(self, ctx: CGrammarParser.DereffedvariableContext):
        # print("visitDereffedvariable")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#binOpPrio1.
    def visitBinOpPrio1(self, ctx: CGrammarParser.BinOpPrio1Context):
        # print("visitBinOpPrio1")
        if ctx.PLUS():
            a = BinPlusNode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.MIN():
            a = BinMinNode()
            self.addMetaData(ctx, a)
            return a
        else:
            raise ValueError("Unknown Node")

    # Visit a parse tree produced by CGrammarParser#binOpPrio2.
    def visitBinOpPrio2(self, ctx: CGrammarParser.BinOpPrio2Context):
        # print("visitBinOpPrio2")
        if ctx.DIS():
            a = BinDisNode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.mul():
            a = BinMulNode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.MOD():
            a = BinModNode()
            self.addMetaData(ctx, a)
            return a
        else:
            raise ValueError("Unknown Node")

    # Visit a parse tree produced by CGrammarParser#unOp.
    def visitUnOp(self, ctx: CGrammarParser.UnOpContext):
        # print("visitUnOp")
        if ctx.MIN():
            a = UnMinNode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.PLUS():
            a = UnPlusNode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.NOT():
            a = UnNotNode()
            self.addMetaData(ctx, a)
            return a

    # Visit a parse tree produced by CGrammarParser#logOp.
    def visitLogOp(self, ctx: CGrammarParser.LogOpContext):
        # print("visitLogOp")
        if ctx.AND():
            a = BinAndNode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.OR():
            a = BinOrNode()
            self.addMetaData(ctx, a)
            return a

    # Visit a parse tree produced by CGrammarParser#compOp.
    def visitCompOp(self, ctx: CGrammarParser.CompOpContext):
        # print("visitCompOp")

        if ctx.EQ():
            a = BinEQNode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.GTE():
            a = BinGTENode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.GT():
            a = BinGTNode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.LT():
            a = BinLTNode()
            self.addMetaData(ctx, a)
            return a
        elif ctx.LTE():
            a = BinLTENode()
            self.addMetaData(ctx, a)
            return BinLTENode()
        elif ctx.NE():
            a = BinNENode()
            self.addMetaData(ctx, a)
            return a

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
        node = copy.deepcopy(self.symbol_table.getVar(varname=ctx.getText()))
        self.addMetaData(ctx, node)
        return node

    # Visit a parse tree produced by CGrammarParser#types_specifier.
    def visitTypes_specifier(self, ctx: CGrammarParser.Types_specifierContext):
        # print("visitTypes_specifier")
        if ctx.CHARTYPE():
            node = VariableCharNode()
            self.addMetaData(ctx, node)
            return node
        elif ctx.FLOATTYPE():
            node = VariableFloatNode()
            self.addMetaData(ctx, node)
            return node
        elif ctx.INTTYPE():
            node = VariableIntNode()
            self.addMetaData(ctx, node)
            return node

    # Visit a parse tree produced by CGrammarParser#literal.
    def visitLiteral(self, ctx: CGrammarParser.LiteralContext):
        # print("visitLiteral")
        if ctx.INTLit():
            node = TermIntNode(int(ctx.INTLit().getText()))
            self.addMetaData(ctx, node)
            return node
        elif ctx.FLOATLit():
            value = ctx.FLOATLit().getText()
            floatex = value[-1]
            if floatex == 'f':
                node = TermFloatNode(float(value[:-1]))
                self.addMetaData(ctx, node)
                return node
            node = TermFloatNode(float(value))
            self.addMetaData(ctx, node)
            return node
        elif ctx.CHARLit():
            node = TermCharNode(ctx.CHARLit().getText()[1:-1])
            self.addMetaData(ctx, node)
            return node

    # Visit a parse tree produced by CGrammarParser#const_qualifier.
    def visitConst_qualifier(self, ctx: CGrammarParser.Const_qualifierContext):
        # print("visitConst_qualifier")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CGrammarParser#printf.
    def visitPrintf(self, ctx: CGrammarParser.PrintfContext):
        # print("visitPrintf")
        node = PrintfNode()
        c = ctx.arguments()
        astchild = self.visit(c)
        node.addArgument(astchild)
        if self.counter > 0 and self.counter != len(node.getArguments().getChildren()) - 1:
            raise functionCallargumentMismatch
        self.addMetaData(ctx, node)
        return node

    def visitArguments(self, ctx: CGrammarParser.ArgumentsContext):
        node = ArgumentsNode()
        children = ctx.arg()
        for c in children:
            astchild = self.visit(c)
            node.addChild(astchild)
        self.addMetaData(ctx, node)
        return node

    def visitArg(self, ctx: CGrammarParser.ArgContext):
        return self.visitChildren(ctx)

    def visitString(self, ctx: CGrammarParser.StringContext):
        node = StringNode()
        pointernode = PointerNode(node)
        self.counter = 0
        firstnode = node
        node.setParent(pointernode)
        string = ctx.getText()
        escaped = False
        for char in string:
            if char == "%":
                self.counter += 1
            if char != '"':
                if char == '\\' and not escaped:
                    escaped = True
                    temp = char
                    continue
                if escaped:
                    char = bytes("\\" + char, "utf-8").decode("unicode_escape")

                node.setNext(StringNode())
                node.setValue(char)
                node.getNext().setParent(node)
                node = node.getNext()
                escaped = False
        node = node.parent
        node.setNext(None)
        a = firstnode.getFullString()

        self.addMetaData(ctx, pointernode)
        return pointernode

    def visitFile(self, ctx: CGrammarParser.FileContext):
        node1 = CodeblockNode()
        if self.symbol_table:
            self.symbol_table.addChild(node1.getSymbolTable())
        self.symbol_table = node1.getSymbolTable()
        for c in ctx.getChildren():
            astchild = self.visit(c)
            if astchild:
                node1.addchild(astchild)
        if self.symbol_table.parent:
            self.symbol_table = self.symbol_table.parent
        self.addMetaData(ctx, node1)
        return node1

    def visitStatement(self, ctx: CGrammarParser.StatementContext):
        # node1 = StatementNode()
        # for c in ctx.getChildren():
        #     astchild = self.visit(c)
        #     if astchild:
        #         node1.addChild(astchild)
        return self.visitChildren(ctx)

    def visitIfstatement(self, ctx: CGrammarParser.IfstatementContext):
        # condition = ConditionNode()
        node = IfstatementNode()
        self.pushSymbolTable(node.symbol_table)
        child = self.visit(ctx.expr())
        # condition.addChild(child)
        codeblock = self.visit(ctx.body())
        node.setCondition(child)
        node.setBlock(codeblock)
        self.popSymbolTable()
        self.addMetaData(ctx, node)

        return node

    def visitIfelsestatement(self, ctx: CGrammarParser.IfelsestatementContext):
        ifnode = self.visit(ctx.ifstatement())
        elsenode = self.visit(ctx.elsestatement())
        node = IfElseStatementNode(ifnode, elsenode)
        self.addMetaData(ctx, node)
        return node

    def visitElsestatement(self, ctx: CGrammarParser.ElsestatementContext):
        node = ElsestatementNode()
        codeblock = self.visit(ctx.body())
        node.setBlock(codeblock)
        self.addMetaData(ctx, node)
        return node

    def visitWhilestatement(self, ctx: CGrammarParser.WhilestatementContext):
        node = WhilestatementNode()
        child = self.visit(ctx.expr())
        codeblock = self.visit(ctx.body())
        node.setCondition(child)
        node.setBlock(codeblock)
        self.addMetaData(ctx, node)
        return node

    def visitCondition(self, ctx: CGrammarParser.ConditionContext):
        return self.visit(ctx.expr())

    def visitInitializer(self, ctx: CGrammarParser.InitializerContext):
        return self.visit(ctx.expr())

    def visitIncrementer(self, ctx: CGrammarParser.IncrementerContext):
        return self.visit(ctx.expr())

    def visitForstatement(self, ctx: CGrammarParser.ForstatementContext):
        node = WhilestatementNode()
        initializer = self.visit(ctx.initializer())
        condition = self.visit(ctx.condition())
        incrementer = self.visit(ctx.incrementer())

        codeblock: CodeblockNode = self.visit(ctx.body())
        codeblock.addchild(incrementer)
        node.setCondition(condition)
        node.setBlock(codeblock)
        self.addMetaData(ctx, node)
        return initializer, node

    def visitBody(self, ctx: CGrammarParser.BodyContext):
        node1 = CodeblockNode()
        _break = False
        _continue = False
        if self.symbol_table:
            self.symbol_table.addChild(node1.getSymbolTable())
        self.symbol_table = node1.getSymbolTable()
        for c in ctx.getChildren():
            astchild = self.visit(c)
            if _break or _continue:
                continue
            elif c.getText() == "break":
                astchild = BreakNode()
                astchild.setParent(node1)
                node1.addchild(astchild)
                _break = True
            elif c.getText() == "continue":
                astchild = ContinueNode()
                astchild.setParent(node1)
                node1.addchild(astchild)
                _continue = True
            elif astchild:
                node1.addchild(astchild)
        if self.symbol_table.parent:
            self.symbol_table = self.symbol_table.parent
        self.addMetaData(ctx, node1)
        return node1

    def pushSymbolTable(self, new_symbol_table):
        new_symbol_table.parent = self.symbol_table
        self.symbol_table.addChild(new_symbol_table)
        self.symbol_table = new_symbol_table

    def popSymbolTable(self):
        if self.symbol_table.parent:
            self.symbol_table = self.symbol_table.parent

    def visitFunctiondefinition(self, ctx: CGrammarParser.FunctiondefinitionContext):
        _type = ctx.getChild(0).getText()
        _name = ctx.getChild(1).getText()
        _arguments = ctx.arguments()

        node = FunctionDefinition(_name, _type)

        if _arguments:
            if self.symbol_table:
                self.symbol_table.addChild(node.getSymbolTable())
                self.symbol_table = node.getSymbolTable()
            _arguments = self.visit(_arguments)
            node.addArgument(_arguments)
        self.pushSymbolTable(SymbolTable())
        body = self.visitFunctionbody(ctx.functionbody())
        node.setFunctionbody(body)
        node.checkReturn()
        node.setSymbolTabel(self.symbol_table)
        self.popSymbolTable()
        self.symbol_table.appendFunction(node)
        if _name == "main":
            self.setVisitedMain()
        self.addMetaData(ctx, node)
        return node

    def visitFunctionbody(self, ctx: CGrammarParser.FunctionbodyContext):
        node = FunctionBody()
        _return = ReturnNode()
        ret = False
        dead = False
        for c in ctx.getChildren():
            astchild = self.visit(c)
            if c.getText() == "return":
                node.addBody(_return)
                ret = True
            elif dead:
                continue
            elif ret and astchild and not dead:
                _return.setChild(astchild)
                dead = True
            elif astchild:
                if isinstance(astchild, tuple):
                    for astc in astchild:
                        node.addBody(astc)
                else:
                    node.addBody(astchild)

        self.addMetaData(ctx, node)
        return node

    def visitFunctioncall(self, ctx: CGrammarParser.FunctioncallContext):
        name = ctx.getChild(0).getText()
        node = FunctionCall(name)
        arguments = ctx.arguments()
        if arguments:
            node.addArgument(self.visit(arguments))

        if not self.symbol_table.getFunction(node.getName()):
            raise UninitializedException(name)

        self.addMetaData(ctx, node)
        return node

    def visitInclude(self, ctx: CGrammarParser.IncludeContext):
        node = IncludeNode()
        node.setLibrary(self.visit(ctx.library()))
        self.addMetaData(ctx, node)
        return node

    def visitLibrary(self, ctx: CGrammarParser.LibraryContext):
        name = ctx.getText()
        node = LibraryNode(name)
        self.addMetaData(ctx, node)
        return node

    def visitFunctiondeclaration(self, ctx: CGrammarParser.FunctiondeclarationContext):
        _type = ctx.getChild(0).getText()
        _name = ctx.getChild(1).getText()
        _arguments = ctx.arguments()

        node = FunctionDefinition(_name, _type)
        if _arguments:
            if self.symbol_table:
                self.symbol_table.addChild(node.getSymbolTable())
                self.symbol_table = node.getSymbolTable()
            _arguments = self.visit(_arguments)
            node.addArgument(_arguments)
        node.checkReturn()
        if self.symbol_table.parent:
            self.symbol_table = self.symbol_table.parent
        self.symbol_table.appendFunction(node)
        if _name == "main":
            self.setVisitedMain()
        self.addMetaData(ctx, node)
        return node

    # def findNode(self, name: str):
    #     deref_count = 0
    #     for c in name:
    #         if c == '*':
    #             deref_count = + 1
    #         else:
    #             break
    #     name = name[deref_count:]
    #     s = self._symbol_table.getVar(varname=name)
    #     for i in range(0, deref_count):
    #         s = s.deRef()
    #     return s

    def setVisitedMain(self):
        self.visitedmain = True

    def getVisitedMain(self):
        return self.visitedmain


del CGrammarParser
