# Generated from ./g4_files/MathExpr.g4 by ANTLR 4.9.3
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3")
        buf.write(u"\6\20\4\2\t\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2\13\n\2\f\2")
        buf.write(u"\16\2\16\13\2\3\2\2\3\2\3\2\2\2\2\17\2\4\3\2\2\2\4\5")
        buf.write(u"\b\2\1\2\5\6\7\3\2\2\6\f\3\2\2\2\7\b\f\4\2\2\b\t\7\5")
        buf.write(u"\2\2\t\13\5\2\2\5\n\7\3\2\2\2\13\16\3\2\2\2\f\n\3\2\2")
        buf.write(u"\2\f\r\3\2\2\2\r\3\3\2\2\2\16\f\3\2\2\2\3\f")
        return buf.getvalue()


class MathExprParser ( Parser ):

    grammarFileName = "MathExpr.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ u"<INVALID>", u"INT", u"MUL", u"SUM", u"WS" ]

    RULE_expr = 0

    ruleNames =  [ u"expr" ]

    EOF = Token.EOF
    INT=1
    MUL=2
    SUM=3
    WS=4

    def __init__(self, input, output=sys.stdout):
        super(MathExprParser, self).__init__(input, output=output)
        self.checkVersion("4.9.3")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MathExprParser.ExprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(MathExprParser.INT, 0)

        def expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(MathExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(MathExprParser.ExprContext,i)


        def SUM(self):
            return self.getToken(MathExprParser.SUM, 0)

        def getRuleIndex(self):
            return MathExprParser.RULE_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterExpr"):
                listener.enterExpr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitExpr"):
                listener.exitExpr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitExpr"):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = MathExprParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 3
            self.match(MathExprParser.INT)
            self._ctx.stop = self._input.LT(-1)
            self.state = 10
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = MathExprParser.ExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                    self.state = 5
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 6
                    self.match(MathExprParser.SUM)
                    self.state = 7
                    self.expr(3) 
                self.state = 12
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx, ruleIndex, predIndex):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx, predIndex):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         




