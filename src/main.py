import sys
from antlr4 import *
from g4_files.MathExprLexer import MathExprLexer
from g4_files.MathExprParser import MathExprParser
from AST import AST
import graphviz


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = MathExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MathExprParser(stream)
    tree = parser.startRule()
    a = AST(tree=tree,name="a")
    dot = a.toDot()
    a.fold()
    dot = a.toDot()



if __name__ == '__main__':
    main(sys.argv)