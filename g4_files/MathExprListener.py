# Generated from ./g4_files/MathExpr.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MathExprParser import MathExprParser
else:
    from MathExprParser import MathExprParser

# This class defines a complete listener for a parse tree produced by MathExprParser.
class MathExprListener(ParseTreeListener):

    # Enter a parse tree produced by MathExprParser#startRule.
    def enterStartRule(self, ctx:MathExprParser.StartRuleContext):
        pass

    # Exit a parse tree produced by MathExprParser#startRule.
    def exitStartRule(self, ctx:MathExprParser.StartRuleContext):
        pass


    # Enter a parse tree produced by MathExprParser#expr.
    def enterExpr(self, ctx:MathExprParser.ExprContext):
        pass

    # Exit a parse tree produced by MathExprParser#expr.
    def exitExpr(self, ctx:MathExprParser.ExprContext):
        pass


    # Enter a parse tree produced by MathExprParser#binOp.
    def enterBinOp(self, ctx:MathExprParser.BinOpContext):
        pass

    # Exit a parse tree produced by MathExprParser#binOp.
    def exitBinOp(self, ctx:MathExprParser.BinOpContext):
        pass


    # Enter a parse tree produced by MathExprParser#unOp.
    def enterUnOp(self, ctx:MathExprParser.UnOpContext):
        pass

    # Exit a parse tree produced by MathExprParser#unOp.
    def exitUnOp(self, ctx:MathExprParser.UnOpContext):
        pass


    # Enter a parse tree produced by MathExprParser#logOp.
    def enterLogOp(self, ctx:MathExprParser.LogOpContext):
        pass

    # Exit a parse tree produced by MathExprParser#logOp.
    def exitLogOp(self, ctx:MathExprParser.LogOpContext):
        pass


    # Enter a parse tree produced by MathExprParser#compOp.
    def enterCompOp(self, ctx:MathExprParser.CompOpContext):
        pass

    # Exit a parse tree produced by MathExprParser#compOp.
    def exitCompOp(self, ctx:MathExprParser.CompOpContext):
        pass



del MathExprParser