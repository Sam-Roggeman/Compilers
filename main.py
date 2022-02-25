import sys
from antlr4 import *
from g4_files.MathExprLexer import MathExprLexer
from g4_files.MathExprParser import MathExprParser
MathExprLexer

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = MathExprParser(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MathExprParser(stream)
    tree = parser.startRule()


if __name__ == '__main__':
    main(sys.argv)