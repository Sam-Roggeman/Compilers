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
        buf.write("<\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2")
        buf.write("\7\2\20\n\2\f\2\16\2\23\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\5\3\37\n\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\3\3\7\3/\n\3\f\3\16\3\62\13\3")
        buf.write("\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\7\2\3\4\b\2\4\6\b\n")
        buf.write("\f\2\b\5\2\5\5\7\7\17\17\5\2\4\4\6\6\23\23\4\2\5\5\7\7")
        buf.write("\3\2\r\16\4\2\b\n\20\22\4\2\4\7\23\23\2=\2\21\3\2\2\2")
        buf.write("\4\36\3\2\2\2\6\63\3\2\2\2\b\65\3\2\2\2\n\67\3\2\2\2\f")
        buf.write("9\3\2\2\2\16\20\5\4\3\2\17\16\3\2\2\2\20\23\3\2\2\2\21")
        buf.write("\17\3\2\2\2\21\22\3\2\2\2\22\24\3\2\2\2\23\21\3\2\2\2")
        buf.write("\24\25\7\2\2\3\25\3\3\2\2\2\26\27\b\3\1\2\27\30\t\2\2")
        buf.write("\2\30\37\5\4\3\b\31\32\7\13\2\2\32\33\5\4\3\2\33\34\7")
        buf.write("\f\2\2\34\37\3\2\2\2\35\37\7\3\2\2\36\26\3\2\2\2\36\31")
        buf.write("\3\2\2\2\36\35\3\2\2\2\37\60\3\2\2\2 !\f\n\2\2!\"\t\3")
        buf.write("\2\2\"/\5\4\3\13#$\f\t\2\2$%\t\4\2\2%/\5\4\3\n&\'\f\7")
        buf.write("\2\2\'(\t\5\2\2(/\5\4\3\b)*\f\6\2\2*+\t\6\2\2+/\5\4\3")
        buf.write("\7,-\f\4\2\2-/\7\24\2\2. \3\2\2\2.#\3\2\2\2.&\3\2\2\2")
        buf.write(".)\3\2\2\2.,\3\2\2\2/\62\3\2\2\2\60.\3\2\2\2\60\61\3\2")
        buf.write("\2\2\61\5\3\2\2\2\62\60\3\2\2\2\63\64\t\7\2\2\64\7\3\2")
        buf.write("\2\2\65\66\t\4\2\2\66\t\3\2\2\2\678\t\5\2\28\13\3\2\2")
        buf.write("\29:\t\6\2\2:\r\3\2\2\2\6\21\36.\60")
        return buf.getvalue()


class MathExprParser ( Parser ):

    grammarFileName = "MathExpr.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'*'", "'-'", "'/'", "'+'", 
                     "'<'", "'>'", "'=='", "'('", "')'", "'&&'", "'||'", 
                     "'!'", "'<='", "'>='", "'!='", "'%'", "';'" ]

    symbolicNames = [ "<INVALID>", "INT", "MUL", "MIN", "DIS", "PLUS", "LT", 
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
    MIN=3
    DIS=4
    PLUS=5
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

        def EOF(self):
            return self.getToken(MathExprParser.EOF, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MathExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(MathExprParser.ExprContext,i)


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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MathExprParser.INT) | (1 << MathExprParser.MIN) | (1 << MathExprParser.PLUS) | (1 << MathExprParser.LBR) | (1 << MathExprParser.NOT))) != 0):
                self.state = 12
                self.expr(0)
                self.state = 17
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 18
            self.match(MathExprParser.EOF)
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

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MathExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(MathExprParser.ExprContext,i)


        def PLUS(self):
            return self.getToken(MathExprParser.PLUS, 0)

        def MIN(self):
            return self.getToken(MathExprParser.MIN, 0)

        def NOT(self):
            return self.getToken(MathExprParser.NOT, 0)

        def LBR(self):
            return self.getToken(MathExprParser.LBR, 0)

        def RBR(self):
            return self.getToken(MathExprParser.RBR, 0)

        def INT(self):
            return self.getToken(MathExprParser.INT, 0)

        def MUL(self):
            return self.getToken(MathExprParser.MUL, 0)

        def DIS(self):
            return self.getToken(MathExprParser.DIS, 0)

        def MOD(self):
            return self.getToken(MathExprParser.MOD, 0)

        def AND(self):
            return self.getToken(MathExprParser.AND, 0)

        def OR(self):
            return self.getToken(MathExprParser.OR, 0)

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

        def SEMICOL(self):
            return self.getToken(MathExprParser.SEMICOL, 0)

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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [MathExprParser.MIN, MathExprParser.PLUS, MathExprParser.NOT]:
                self.state = 21
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MathExprParser.MIN) | (1 << MathExprParser.PLUS) | (1 << MathExprParser.NOT))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 22
                self.expr(6)
                pass
            elif token in [MathExprParser.LBR]:
                self.state = 23
                self.match(MathExprParser.LBR)
                self.state = 24
                self.expr(0)
                self.state = 25
                self.match(MathExprParser.RBR)
                pass
            elif token in [MathExprParser.INT]:
                self.state = 27
                self.match(MathExprParser.INT)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 46
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 44
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = MathExprParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 30
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 31
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MathExprParser.MUL) | (1 << MathExprParser.DIS) | (1 << MathExprParser.MOD))) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 32
                        self.expr(9)
                        pass

                    elif la_ == 2:
                        localctx = MathExprParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 33
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 34
                        _la = self._input.LA(1)
                        if not(_la==MathExprParser.MIN or _la==MathExprParser.PLUS):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 35
                        self.expr(8)
                        pass

                    elif la_ == 3:
                        localctx = MathExprParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 36
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 37
                        _la = self._input.LA(1)
                        if not(_la==MathExprParser.AND or _la==MathExprParser.OR):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 38
                        self.expr(6)
                        pass

                    elif la_ == 4:
                        localctx = MathExprParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 39
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 40
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MathExprParser.LT) | (1 << MathExprParser.GT) | (1 << MathExprParser.EQ) | (1 << MathExprParser.LTE) | (1 << MathExprParser.GTE) | (1 << MathExprParser.NE))) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 41
                        self.expr(5)
                        pass

                    elif la_ == 5:
                        localctx = MathExprParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 42
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 43
                        self.match(MathExprParser.SEMICOL)
                        pass

             
                self.state = 48
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

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
            self.state = 49
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MathExprParser.MUL) | (1 << MathExprParser.MIN) | (1 << MathExprParser.DIS) | (1 << MathExprParser.PLUS) | (1 << MathExprParser.MOD))) != 0)):
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
            self.state = 51
            _la = self._input.LA(1)
            if not(_la==MathExprParser.MIN or _la==MathExprParser.PLUS):
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
            self.state = 53
            _la = self._input.LA(1)
            if not(_la==MathExprParser.AND or _la==MathExprParser.OR):
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
            self.state = 55
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
                return self.precpred(self._ctx, 8)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 2)
         




