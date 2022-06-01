class MetaData:
    _line: int
    _col: int

    def __init__(self, line: int = -1, start_character: int = -1):
        self._line = line
        self._start_c = start_character

    def getLine(self):
        return self._line

    def setLine(self, line: int):
        self._line = line

    def getColumn(self):
        return self._col
