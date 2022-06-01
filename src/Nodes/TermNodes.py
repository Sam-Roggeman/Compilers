from Nodes.AbsNode import *


class TermNode(AbsNode):
    def getSolvedType(self) -> type:
        return type(self)

    @staticmethod
    def getLLVMType():
        pass

    def checkParent(self, parent):
        if not self.parent:
            self.setParent(parent)

    def __str__(self):
        return str(self.value)

    def setValue(self, value):
        if value is not None:
            self.value = value

    def getValue(self):
        return self

    @staticmethod
    def convertNode(child):
        return child

    def __init__(self, value=None):
        super().__init__()
        self.value = None
        self.setValue(value)
        self._lvalue = False

    def __invert__(self):
        if self.value:
            return TermIntNode(1)
        return TermIntNode(0)

    def __add__(self, other):
        # richest_type = richest(type(self),type(other))
        b = copy.deepcopy(self)
        other = self.convertNode(other)
        b.setValue(self.value + other.value)
        return b

    def __sub__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value - other.value)
        return self

    def __mul__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value * other.value)
        return self

    def __truediv__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value / other.value)

        return self

    def __lt__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value < other.value)

    def __mod__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value % other.value)
        return self

    def __gt__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value > other.value)

    def __le__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value <= other.value)

    def __ge__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value >= other.value)

    def __eq__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value == other.value)

    def __ne__(self, other):
        other = self.convertNode(other)
        return TermIntNode(self.value != other.value)

    def __neg__(self):
        self.setValue(-self.value)
        return self

    def __pos__(self, other):
        other = self.convertNode(other)
        return self

    def __and__(self, other):
        other = self.convertNode(other)
        if self.value and other.value:
            return TermIntNode(1)
        return TermIntNode(0)

    def __or__(self, other):
        other = self.convertNode(other)
        if self.value or other.value:
            return TermIntNode(1)
        return TermIntNode(0)

    # def __bool__(self):
    #     return self.value == 0

    def fold(self):
        return self

    def llvmValue(self):
        pass


class TermIntNode(TermNode):
    def __truediv__(self, other):
        other = self.convertNode(other)
        self.setValue(self.value // other.value)
        return self

    def llvmValue(self):
        return ir.Constant(i32, self.value)

    def __init__(self, value: int = None):
        super().__init__()
        self.setValue(value)

    def setValue(self, value: int):
        if value is not None:
            if isinstance(value, bool):
                if value:
                    self.value = 1
                    return
                self.value = 0
                return
            self.value = int(value)
    def toString(self):
        return "i32" + str(self.value)

    @staticmethod
    def convertNode(child: TermNode):
        if isinstance(child, TermIntNode):
            return child
        elif isinstance(child, TermFloatNode):
            # warning
            sys.stderr.write("Warning: Implicit conversion from float to int, possible loss of information" + "\n")
            nchild = TermIntNode(int(child.value))
            # nchild.addMetaData(child.getMetaData())
            return nchild
        elif isinstance(child, TermCharNode):
            nchild = TermIntNode(ord(child.value))
            # nchild.addMetaData(child.getMetaData())
            return nchild
        return child

    @staticmethod
    def getLLVMType():
        return i32


class TermFloatNode(TermNode):
    def llvmValue(self):
        return ir.Constant(cfloat, self.value)

    def __init__(self, value: float = None):
        super().__init__(value)

    def setValue(self, _value: float):
        _value = float(_value)

        super().setValue(_value)

    def toString(self):
        return "cfloat" + str(self.value)

    @staticmethod
    def convertNode(child: TermNode):
        if isinstance(child, TermFloatNode):
            return child
        elif isinstance(child, TermIntNode):
            nchild = TermFloatNode(float(child.value))
            # nchild.addMetaData(child.getMetaData())
            return nchild

        elif isinstance(child, TermCharNode):
            nchild = TermFloatNode(float(ord(child.value)))
            nchild.addMetaData(child.getMetaData())
            return nchild
        return child

    @staticmethod
    def getLLVMType():
        return cfloat


class TermCharNode(TermNode):
    @staticmethod
    def getLLVMType():
        return cchar

    def llvmValue(self):
        intvalue = ord(self.value)

        return ir.Constant(cchar, intvalue)

    def setValue(self, _value: str):
        _value = str(_value)

        if len(_value) == 1:
            super().setValue(_value)

    def __init__(self, value: str = None):
        super().__init__(value)

    def toString(self):
        return "cchar" + str(self.value)

    def fold(self):
        return self

    def convertNode(self, child: TermNode):
        if isinstance(child, TermCharNode):
            return child
        elif isinstance(child, TermFloatNode):
            sys.stderr.write("Warning: Implicit conversion from float to char, possible loss of information " + "\n")
            nchild = TermCharNode(chr(int(child.value)))
            # nchild.addMetaData(child.getMetaData())
            return nchild
        elif isinstance(child, TermIntNode):
            sys.stderr.write("Warning: Implicit conversion from int to char, possible loss of information " + "\n")
            nchild = TermCharNode(chr(child.value))
            # nchild.addMetaData(child.getMetaData())
            return nchild
        return child