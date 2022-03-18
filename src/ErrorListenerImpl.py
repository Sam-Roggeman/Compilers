from antlr4.error.ErrorListener import *

class ErrorListenerImpl(ConsoleErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("line " + str(line) + ":" + str(column) + " " + msg, file=sys.stderr)
