# Generated from ./examples/JSON.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .JSONParser import JSONParser
else:
    from JSONParser import JSONParser

# This class defines a complete generic visitor for a parse tree produced by JSONParser.

class JSONVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JSONParser#json.
    def visitJson(self, ctx:JSONParser.JsonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSONParser#object.
    def visitObject(self, ctx:JSONParser.ObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSONParser#pair.
    def visitPair(self, ctx:JSONParser.PairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSONParser#array.
    def visitArray(self, ctx:JSONParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSONParser#value.
    def visitValue(self, ctx:JSONParser.ValueContext):
        return self.visitChildren(ctx)



del JSONParser