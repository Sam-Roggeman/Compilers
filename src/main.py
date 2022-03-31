import sys
from antlr4 import *

from g4_files.CGrammar2Lexer import CGrammar2Lexer
from g4_files.CGrammar2Parser import CGrammar2Parser
from CSTVisitor import CGrammar2VisitorImplementation
from AST import *
from ASTVisitor import *


def main(argv):
    name = argv[1]
    inputlocation = name
    if "./inputFiles/" not in name:
        inputlocation = "./inputFiles/" + name
    else:
        name = name[13:-2]

    input_stream = FileStream(inputlocation)
    lexer = CGrammar2Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CGrammar2Parser(stream)
    tree = parser.startRule()
    visitor = CGrammar2VisitorImplementation()
    a = AST(root=visitor.visitStartRule(ctx=tree),name=name,symbol_table= visitor.getSymbolTable())

    # a = AST(tree=tree, name=name)
    print("#PreOrder before optimize")
    print(a.preOrderTraversal(oneline=True))
    a.optimize()
    print("#Preorder after optimalizations")
    print(a.preOrderTraversal(oneline=True))


if __name__ == '__main__':
    main(sys.argv)
