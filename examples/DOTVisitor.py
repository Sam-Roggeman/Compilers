# Generated from ./examples/DOT.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DOTParser import DOTParser
else:
    from DOTParser import DOTParser

# This class defines a complete generic visitor for a parse tree produced by DOTParser.

class DOTVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DOTParser#graph.
    def visitGraph(self, ctx:DOTParser.GraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#stmt_list.
    def visitStmt_list(self, ctx:DOTParser.Stmt_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#stmt.
    def visitStmt(self, ctx:DOTParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#attr_stmt.
    def visitAttr_stmt(self, ctx:DOTParser.Attr_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#attr_list.
    def visitAttr_list(self, ctx:DOTParser.Attr_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#a_list.
    def visitA_list(self, ctx:DOTParser.A_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#edge_stmt.
    def visitEdge_stmt(self, ctx:DOTParser.Edge_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#edgeRHS.
    def visitEdgeRHS(self, ctx:DOTParser.EdgeRHSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#edgeop.
    def visitEdgeop(self, ctx:DOTParser.EdgeopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#node_stmt.
    def visitNode_stmt(self, ctx:DOTParser.Node_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#node_id.
    def visitNode_id(self, ctx:DOTParser.Node_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#port.
    def visitPort(self, ctx:DOTParser.PortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#subgraph.
    def visitSubgraph(self, ctx:DOTParser.SubgraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#id.
    def visitId(self, ctx:DOTParser.IdContext):
        return self.visitChildren(ctx)



del DOTParser