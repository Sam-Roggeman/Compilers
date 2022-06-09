class MetaData:
    _line: int
    _col: int
    _stop_line: int
    _stop_col: int

    def __init__(self, line: int = -1, start_character: int = -1, end_line=-1, end_character=-1):
        self._line = line
        self._col = start_character
        self._stop_line = end_line
        self._stop_col = end_character

    def getLine(self):
        return self._line

    def setLine(self, line: int):
        self._line = line

    def getStopLine(self):
        return self._stop_line

    def getColumn(self):
        return self._col

    def getStopCol(self):
        return self._stop_col
