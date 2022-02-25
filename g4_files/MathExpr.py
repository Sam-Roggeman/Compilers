# Generated from ./g4_files/MathExpr.g4 by ANTLR 4.9.3
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2")
        buf.write(u"\4\30\b\1\4\2\t\2\4\3\t\3\3\2\3\2\3\2\7\2\13\n\2\f\2")
        buf.write(u"\16\2\16\13\2\5\2\20\n\2\3\3\6\3\23\n\3\r\3\16\3\24\3")
        buf.write(u"\3\3\3\2\2\4\3\3\5\4\3\2\5\3\2\63;\3\2\62;\5\2\13\f\17")
        buf.write(u"\17\"\"\2\32\2\3\3\2\2\2\2\5\3\2\2\2\3\17\3\2\2\2\5\22")
        buf.write(u"\3\2\2\2\7\20\7\62\2\2\b\f\t\2\2\2\t\13\t\3\2\2\n\t\3")
        buf.write(u"\2\2\2\13\16\3\2\2\2\f\n\3\2\2\2\f\r\3\2\2\2\r\20\3\2")
        buf.write(u"\2\2\16\f\3\2\2\2\17\7\3\2\2\2\17\b\3\2\2\2\20\4\3\2")
        buf.write(u"\2\2\21\23\t\4\2\2\22\21\3\2\2\2\23\24\3\2\2\2\24\22")
        buf.write(u"\3\2\2\2\24\25\3\2\2\2\25\26\3\2\2\2\26\27\b\3\2\2\27")
        buf.write(u"\6\3\2\2\2\6\2\f\17\24\3\b\2\2")
        return buf.getvalue()


class MathExpr(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    INT = 1
    WS = 2

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
 ]

    symbolicNames = [ u"<INVALID>",
            u"INT", u"WS" ]

    ruleNames = [ u"INT", u"WS" ]

    grammarFileName = u"MathExpr.g4"

    def __init__(self, input=None, output=sys.stdout):
        super(MathExpr, self).__init__(input, output=output)
        self.checkVersion("4.9.3")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


