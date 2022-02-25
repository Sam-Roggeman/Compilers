# Generated from ./g4_files/MathExpr.g4 by ANTLR 4.9.3
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\25")
        buf.write("b\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\3\2\3\2\3\2\7\2-\n\2\f\2\16\2\60\13\2\5\2\62")
        buf.write("\n\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3")
        buf.write("\t\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3\r\3")
        buf.write("\16\3\16\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\22\3\22\3\23\3\23\3\24\6\24]\n\24\r\24\16\24^\3\24")
        buf.write("\3\24\2\2\25\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13")
        buf.write("\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25\3")
        buf.write("\2\5\3\2\63;\3\2\62;\5\2\13\f\17\17\"\"\2d\2\3\3\2\2\2")
        buf.write("\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r")
        buf.write("\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3")
        buf.write("\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2")
        buf.write("\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'")
        buf.write("\3\2\2\2\3\61\3\2\2\2\5\63\3\2\2\2\7\65\3\2\2\2\t\67\3")
        buf.write("\2\2\2\139\3\2\2\2\r;\3\2\2\2\17=\3\2\2\2\21?\3\2\2\2")
        buf.write("\23B\3\2\2\2\25D\3\2\2\2\27F\3\2\2\2\31I\3\2\2\2\33L\3")
        buf.write("\2\2\2\35N\3\2\2\2\37Q\3\2\2\2!T\3\2\2\2#W\3\2\2\2%Y\3")
        buf.write("\2\2\2\'\\\3\2\2\2)\62\7\62\2\2*.\t\2\2\2+-\t\3\2\2,+")
        buf.write("\3\2\2\2-\60\3\2\2\2.,\3\2\2\2./\3\2\2\2/\62\3\2\2\2\60")
        buf.write(".\3\2\2\2\61)\3\2\2\2\61*\3\2\2\2\62\4\3\2\2\2\63\64\7")
        buf.write(",\2\2\64\6\3\2\2\2\65\66\7-\2\2\66\b\3\2\2\2\678\7/\2")
        buf.write("\28\n\3\2\2\29:\7\61\2\2:\f\3\2\2\2;<\7>\2\2<\16\3\2\2")
        buf.write("\2=>\7@\2\2>\20\3\2\2\2?@\7?\2\2@A\7?\2\2A\22\3\2\2\2")
        buf.write("BC\7*\2\2C\24\3\2\2\2DE\7+\2\2E\26\3\2\2\2FG\7(\2\2GH")
        buf.write("\7(\2\2H\30\3\2\2\2IJ\7~\2\2JK\7~\2\2K\32\3\2\2\2LM\7")
        buf.write("#\2\2M\34\3\2\2\2NO\7>\2\2OP\7?\2\2P\36\3\2\2\2QR\7@\2")
        buf.write("\2RS\7?\2\2S \3\2\2\2TU\7#\2\2UV\7?\2\2V\"\3\2\2\2WX\7")
        buf.write("\'\2\2X$\3\2\2\2YZ\7=\2\2Z&\3\2\2\2[]\t\4\2\2\\[\3\2\2")
        buf.write("\2]^\3\2\2\2^\\\3\2\2\2^_\3\2\2\2_`\3\2\2\2`a\b\24\2\2")
        buf.write("a(\3\2\2\2\6\2.\61^\3\b\2\2")
        return buf.getvalue()


class MathExprLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    INT = 1
    MUL = 2
    PLUS = 3
    MIN = 4
    DIS = 5
    LT = 6
    GT = 7
    EQ = 8
    LBR = 9
    RBR = 10
    AND = 11
    OR = 12
    NOT = 13
    LTE = 14
    GTE = 15
    NE = 16
    MOD = 17
    SEMICOL = 18
    WS = 19

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'*'", "'+'", "'-'", "'/'", "'<'", "'>'", "'=='", "'('", "')'", 
            "'&&'", "'||'", "'!'", "'<='", "'>='", "'!='", "'%'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "INT", "MUL", "PLUS", "MIN", "DIS", "LT", "GT", "EQ", "LBR", 
            "RBR", "AND", "OR", "NOT", "LTE", "GTE", "NE", "MOD", "SEMICOL", 
            "WS" ]

    ruleNames = [ "INT", "MUL", "PLUS", "MIN", "DIS", "LT", "GT", "EQ", 
                  "LBR", "RBR", "AND", "OR", "NOT", "LTE", "GTE", "NE", 
                  "MOD", "SEMICOL", "WS" ]

    grammarFileName = "MathExpr.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


