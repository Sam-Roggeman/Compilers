# Generated from ./g4_files/MathExpr.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MathExprParser import MathExprParser
else:
    from MathExprParser import MathExprParser

# This class defines a complete generic visitor for a parse tree produced by MathExprParser.

class MathExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MathExprParser#startRule.
    def visitStartRule(self, ctx:MathExprParser.StartRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MathExprParser#expr.
    def visitExpr(self, ctx:MathExprParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MathExprParser#binOp.
    def visitBinOp(self, ctx:MathExprParser.BinOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MathExprParser#unOp.
    def visitUnOp(self, ctx:MathExprParser.UnOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MathExprParser#logOp.
    def visitLogOp(self, ctx:MathExprParser.LogOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MathExprParser#compOp.
    def visitCompOp(self, ctx:MathExprParser.CompOpContext):
        return self.visitChildren(ctx)



del MathExprParser