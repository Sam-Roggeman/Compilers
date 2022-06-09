from antlr4.error.ErrorListener import *
import sys

# Will inherent de class ErrorListener
class ErrorVisitors(ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        sys.stderr.write("[ERROR] Mismatched input at line: " + str(line) + ", column: " + str(column) + " expecting something other than '" +
              offendingSymbol.text + "'.")
        exit(1)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        pass