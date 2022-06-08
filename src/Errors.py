import copy
from copy import deepcopy
from MetaData import *


class GeneralException(Exception):
    _metadata: MetaData
    varname: str

    def __init__(self, varname: str = "", metadata: MetaData = MetaData()):
        self._metadata = copy.deepcopy(metadata)

        self.varname = varname

    def setVarName(self, v: str):
        self.varname = v

    def setMetaData(self, metadata: MetaData):
        self._metadata = metadata


class ConstException(GeneralException):
    def __str__(self):
        return "error: assignment of read-only variable \"" + self.varname + "\" n line " + str(
            self._metadata.getLine())


class UninitializedException(GeneralException):
    def __str__(self):
        return "error: \"" + self.varname + "\" on line " + str(
            self._metadata.getLine()) + " was not declared in this scope"


class RedefinitionException(GeneralException):
    def __str__(self):
        return "error: redefinition of \"" + self.varname + "\" on line " + str(self._metadata.getLine())


class FunctionRedefinitionException(GeneralException):
    def __str__(self):
        return "error: function redefinition of \"" + self.varname + "\" on line " + str(self._metadata.getLine())


# class IncompatibleException(Exception):
#     type1 = ""
#     type2 = ""
#
#     def __init__(self, type1, type2):
#         super().__init__(varname, metadata)
#         self.type1 = type1
#         self.type2 = type2
#
#     def __str__(self):
#         return "error: invalid conversion from \"" + self.type1 + " to " + self.type2 + "\" on line " + str(
#             self._metadata.getLine())
# 


class RValueException(GeneralException):
    def __str__(self):
        return "error: lvalue required as left operand of assignment" + " on line " + str(self._metadata.getLine())


class returnTypeMismatch(GeneralException):
    def __str__(self):
        return "error: void function does not expect a return" + str(self._metadata.getLine())

class declarationDefinitionMismatch(GeneralException):
    def __str__(self):
        return "error: declaration is not matched with definition/declaration on line " + str(self._metadata.getLine())


class functionCallargumentMismatch(GeneralException):
    def __str__(self):
        return "error: functioncall arguments don't match functiondefinition arguments " + str(self._metadata.getLine())

class mainNotFound(GeneralException):
    def __str__(self):
        return "error: main not found"

class pointerOperationError(GeneralException):
    def __str__(self):
        return "error: invalid operands to binary " + self.varname

