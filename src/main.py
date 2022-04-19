import sys
from antlr4 import *

from g4_files.CGrammarLexer import CGrammarLexer
from g4_files.CGrammarParser import CGrammarParser
from CSTVisitor import CGrammarVisitorImplementation
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
    lexer = CGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CGrammarParser(stream)
    tree = parser.startRule()
    visitor = CGrammarVisitorImplementation()
    a = AST(root=visitor.visitStartRule(ctx=tree),name=name)

    print("#PreOrder before optimize")
    print(a.preOrderTraversal(oneline=True))
    a.toDot(name="start")
    a.optimize()
    print("#Preorder after optimalizations")
    print(a.preOrderTraversal(oneline=True))
    a.exportToLLVM()


if __name__ == '__main__':
    main(sys.argv)
