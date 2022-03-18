import copy
from copy import deepcopy


class MetaData:
    _line: int
    _col: int

    def __init__(self, line:int = -1, start_character:int = -1):
        self._line = line
        self._start_c = start_character

    def getLine(self):
        return self._line

    def setLine(self, line: int):
        self._line = line

    def getColumn(self):
        return self._col


class GeneralException(Exception):
    _metadata: MetaData
    varname: str

    def __init__(self, varname:str = "",metadata: MetaData = MetaData()):
        self._metadata = copy.deepcopy(metadata)

        self.varname = varname

    def setVarName(self, v: str):
        self.varname = v

    def setMetaData(self, metadata: MetaData):
        self._metadata = metadata


class ConstException(GeneralException):
    def __str__(self):
        return "error: assignment of read-only variable \"" + self.varname + "\" n line " + str(self._metadata.getLine())


class UninitializedException(GeneralException):
    def __str__(self):
        return "error: \"" + self.varname + "\" on line " + str(self._metadata.getLine()) + " was not declared in this scope"

class RedefinitionException(GeneralException):
    def __str__(self):
        return "error: redefinition of \"" + self.varname + "\" on line " + str(self._metadata.getLine())

class IncompatibleException(Exception):
    type1 = ""
    type2 = ""
    def __init__(self, type1,type2):
        super().__init__(varname,metadata)
        self.type1 = type1
        self.type2 = type2
    def __str__(self):
        return "error: invalid conversion from \"" + self.type1 + " to " + self.type2 + "\" on line " + str(self._metadata.getLine())

class RValueException(GeneralException):
    def __str__(self):
        return "error: lvalue required as left operand of assignment" + " on line " + str(self._metadata.getLine())