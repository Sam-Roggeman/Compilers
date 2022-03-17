import sys
from antlr4 import *

from g4_files.CGrammarLexer import CGrammarLexer
from g4_files.CGrammarParser import CGrammarParser
from AST import *


def main(argv):
    name = argv[1]
    inputlocation = name
    if "./inputFiles/" not in name:
        inputlocation = "./inputFiles/" + name

    input_stream = FileStream(inputlocation)
    lexer = CGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CGrammarParser(stream)
    tree = parser.startRule()

    a = AST(tree=tree, name=name)
    print("#PreOrder before optimize")
    print(a.preOrderTraversal(True))
    a.optimize()
    print("#Preorder after optimalizations")
    print(a.preOrderTraversal(True))


if __name__ == '__main__':
    main(sys.argv)
