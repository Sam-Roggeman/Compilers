# Generated from ./g4_files/MathExpr.g4 by ANTLR 4.9.3
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2")
        buf.write(u"\6 \b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\3\2\7")
        buf.write(u"\2\17\n\2\f\2\16\2\22\13\2\5\2\24\n\2\3\3\3\3\3\4\3\4")
        buf.write(u"\3\5\6\5\33\n\5\r\5\16\5\34\3\5\3\5\2\2\6\3\3\5\4\7\5")
        buf.write(u"\t\6\3\2\7\3\2\63;\3\2\62;\4\2,,^^\3\2--\5\2\13\f\17")
        buf.write(u"\17\"\"\2\"\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3")
        buf.write(u"\2\2\2\3\23\3\2\2\2\5\25\3\2\2\2\7\27\3\2\2\2\t\32\3")
        buf.write(u"\2\2\2\13\24\7\62\2\2\f\20\t\2\2\2\r\17\t\3\2\2\16\r")
        buf.write(u"\3\2\2\2\17\22\3\2\2\2\20\16\3\2\2\2\20\21\3\2\2\2\21")
        buf.write(u"\24\3\2\2\2\22\20\3\2\2\2\23\13\3\2\2\2\23\f\3\2\2\2")
        buf.write(u"\24\4\3\2\2\2\25\26\t\4\2\2\26\6\3\2\2\2\27\30\t\5\2")
        buf.write(u"\2\30\b\3\2\2\2\31\33\t\6\2\2\32\31\3\2\2\2\33\34\3\2")
        buf.write(u"\2\2\34\32\3\2\2\2\34\35\3\2\2\2\35\36\3\2\2\2\36\37")
        buf.write(u"\b\5\2\2\37\n\3\2\2\2\6\2\20\23\34\3\b\2\2")
        return buf.getvalue()


class MathExprLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    INT = 1
    MUL = 2
    SUM = 3
    WS = 4

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
 ]

    symbolicNames = [ u"<INVALID>",
            u"INT", u"MUL", u"SUM", u"WS" ]

    ruleNames = [ u"INT", u"MUL", u"SUM", u"WS" ]

    grammarFileName = u"MathExpr.g4"

    def __init__(self, input=None, output=sys.stdout):
        super(MathExprLexer, self).__init__(input, output=output)
        self.checkVersion("4.9.3")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


