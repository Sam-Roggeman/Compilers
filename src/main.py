import sys
from antlr4 import *
from g4_files.CGrammarLexer import CGrammarLexer
from g4_files.CGrammarParser import CGrammarParser
from AST import AST
import graphviz


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CGrammarParser(stream)
    tree = parser.startRule()
    a = AST(tree=tree,name="a")
    dot = a.toDot()
    a.fold()
    dot = a.toDot()



if __name__ == '__main__':
    main(sys.argv)
