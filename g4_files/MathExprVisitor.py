# Generated from ./g4_files/MathExpr.g4 by ANTLR 4.9.3
from antlr4 import *

# This class defines a complete generic visitor for a parse tree produced by MathExprParser.

class MathExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MathExprParser#expr.
    def visitExpr(self, ctx):
        return self.visitChildren(ctx)


