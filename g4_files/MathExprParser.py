# Generated from ./g4_files/MathExpr.g4 by ANTLR 4.9.3
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\25")
        buf.write(".\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2")
        buf.write("\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3\33\n")
        buf.write("\3\3\3\3\3\3\3\3\3\7\3!\n\3\f\3\16\3$\13\3\3\4\3\4\3\5")
        buf.write("\3\5\3\6\3\6\3\7\3\7\3\7\2\3\4\b\2\4\6\b\n\f\2\6\4\2\4")
        buf.write("\7\23\23\3\2\5\6\3\2\r\17\4\2\b\n\20\22\2*\2\16\3\2\2")
        buf.write("\2\4\32\3\2\2\2\6%\3\2\2\2\b\'\3\2\2\2\n)\3\2\2\2\f+\3")
        buf.write("\2\2\2\16\17\5\4\3\2\17\20\7\24\2\2\20\3\3\2\2\2\21\22")
        buf.write("\b\3\1\2\22\23\5\b\5\2\23\24\5\4\3\5\24\33\3\2\2\2\25")
        buf.write("\26\7\13\2\2\26\27\5\4\3\2\27\30\7\f\2\2\30\33\3\2\2\2")
        buf.write("\31\33\7\3\2\2\32\21\3\2\2\2\32\25\3\2\2\2\32\31\3\2\2")
        buf.write("\2\33\"\3\2\2\2\34\35\f\6\2\2\35\36\5\6\4\2\36\37\5\4")
        buf.write("\3\7\37!\3\2\2\2 \34\3\2\2\2!$\3\2\2\2\" \3\2\2\2\"#\3")
        buf.write("\2\2\2#\5\3\2\2\2$\"\3\2\2\2%&\t\2\2\2&\7\3\2\2\2\'(\t")
        buf.write("\3\2\2(\t\3\2\2\2)*\t\4\2\2*\13\3\2\2\2+,\t\5\2\2,\r\3")
        buf.write("\2\2\2\4\32\"")
        return buf.getvalue()


class MathExprParser ( Parser ):

    grammarFileName = "MathExpr.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'*'", "'+'", "'-'", "'/'", 
                     "'<'", "'>'", "'=='", "'('", "')'", "'&&'", "'||'", 
                     "'!'", "'<='", "'>='", "'!='", "'%'", "';'" ]

    symbolicNames = [ "<INVALID>", "INT", "MUL", "PLUS", "MIN", "DIS", "LT", 
                      "GT", "EQ", "LBR", "RBR", "AND", "OR", "NOT", "LTE", 
                      "GTE", "NE", "MOD", "SEMICOL", "WS" ]

    RULE_startRule = 0
    RULE_expr = 1
    RULE_binOp = 2
    RULE_unOp = 3
    RULE_logOp = 4
    RULE_compOp = 5

    ruleNames =  [ "startRule", "expr", "binOp", "unOp", "logOp", "compOp" ]

    EOF = Token.EOF
    INT=1
    MUL=2
    PLUS=3
    MIN=4
    DIS=5
    LT=6
    GT=7
    EQ=8
    LBR=9
    RBR=10
    AND=11
    OR=12
    NOT=13
    LTE=14
    GTE=15
    NE=16
    MOD=17
    SEMICOL=18
    WS=19

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartRuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(MathExprParser.ExprContext,0)


        def SEMICOL(self):
            return self.getToken(MathExprParser.SEMICOL, 0)

        def getRuleIndex(self):
            return MathExprParser.RULE_startRule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStartRule" ):
                listener.enterStartRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStartRule" ):
                listener.exitStartRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStartRule" ):
                return visitor.visitStartRule(self)
            else:
                return visitor.visitChildren(self)




    def startRule(self):

        localctx = MathExprParser.StartRuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_startRule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.expr(0)
            self.state = 13
            self.match(MathExprParser.SEMICOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unOp(self):
            return self.getTypedRuleContext(MathExprParser.UnOpContext,0)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MathExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(MathExprParser.ExprContext,i)


        def LBR(self):
            return self.getToken(MathExprParser.LBR, 0)

        def RBR(self):
            return self.getToken(MathExprParser.RBR, 0)

        def INT(self):
            return self.getToken(MathExprParser.INT, 0)

        def binOp(self):
            return self.getTypedRuleContext(MathExprParser.BinOpContext,0)


        def getRuleIndex(self):
            return MathExprParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = MathExprParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [MathExprParser.PLUS, MathExprParser.MIN]:
                self.state = 16
                self.unOp()
                self.state = 17
                self.expr(3)
                pass
            elif token in [MathExprParser.LBR]:
                self.state = 19
                self.match(MathExprParser.LBR)
                self.state = 20
                self.expr(0)
                self.state = 21
                self.match(MathExprParser.RBR)
                pass
            elif token in [MathExprParser.INT]:
                self.state = 23
                self.match(MathExprParser.INT)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 32
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = MathExprParser.ExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                    self.state = 26
                    if not self.precpred(self._ctx, 4):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                    self.state = 27
                    self.binOp()
                    self.state = 28
                    self.expr(5) 
                self.state = 34
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class BinOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(MathExprParser.PLUS, 0)

        def MIN(self):
            return self.getToken(MathExprParser.MIN, 0)

        def DIS(self):
            return self.getToken(MathExprParser.DIS, 0)

        def MUL(self):
            return self.getToken(MathExprParser.MUL, 0)

        def MOD(self):
            return self.getToken(MathExprParser.MOD, 0)

        def getRuleIndex(self):
            return MathExprParser.RULE_binOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinOp" ):
                listener.enterBinOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinOp" ):
                listener.exitBinOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinOp" ):
                return visitor.visitBinOp(self)
            else:
                return visitor.visitChildren(self)




    def binOp(self):

        localctx = MathExprParser.BinOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_binOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MathExprParser.MUL) | (1 << MathExprParser.PLUS) | (1 << MathExprParser.MIN) | (1 << MathExprParser.DIS) | (1 << MathExprParser.MOD))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(MathExprParser.PLUS, 0)

        def MIN(self):
            return self.getToken(MathExprParser.MIN, 0)

        def getRuleIndex(self):
            return MathExprParser.RULE_unOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnOp" ):
                listener.enterUnOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnOp" ):
                listener.exitUnOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnOp" ):
                return visitor.visitUnOp(self)
            else:
                return visitor.visitChildren(self)




    def unOp(self):

        localctx = MathExprParser.UnOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_unOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            _la = self._input.LA(1)
            if not(_la==MathExprParser.PLUS or _la==MathExprParser.MIN):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AND(self):
            return self.getToken(MathExprParser.AND, 0)

        def NOT(self):
            return self.getToken(MathExprParser.NOT, 0)

        def OR(self):
            return self.getToken(MathExprParser.OR, 0)

        def getRuleIndex(self):
            return MathExprParser.RULE_logOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogOp" ):
                listener.enterLogOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogOp" ):
                listener.exitLogOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogOp" ):
                return visitor.visitLogOp(self)
            else:
                return visitor.visitChildren(self)




    def logOp(self):

        localctx = MathExprParser.LogOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_logOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MathExprParser.AND) | (1 << MathExprParser.OR) | (1 << MathExprParser.NOT))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LT(self):
            return self.getToken(MathExprParser.LT, 0)

        def GT(self):
            return self.getToken(MathExprParser.GT, 0)

        def EQ(self):
            return self.getToken(MathExprParser.EQ, 0)

        def LTE(self):
            return self.getToken(MathExprParser.LTE, 0)

        def GTE(self):
            return self.getToken(MathExprParser.GTE, 0)

        def NE(self):
            return self.getToken(MathExprParser.NE, 0)

        def getRuleIndex(self):
            return MathExprParser.RULE_compOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompOp" ):
                listener.enterCompOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompOp" ):
                listener.exitCompOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompOp" ):
                return visitor.visitCompOp(self)
            else:
                return visitor.visitChildren(self)




    def compOp(self):

        localctx = MathExprParser.CompOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_compOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MathExprParser.LT) | (1 << MathExprParser.GT) | (1 << MathExprParser.EQ) | (1 << MathExprParser.LTE) | (1 << MathExprParser.GTE) | (1 << MathExprParser.NE))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         




