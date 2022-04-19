from io import *
from typing import TextIO


class LLVMBuilder:
    _output: TextIO
    _current_reg: int = 1
    _regToType: dict[int:str] = dict()

    def __init__(self, filepath: str):
        self._output = open(file=filepath, mode='w')

    def allocateMemory(self, memory_type: str, size: int):
        self._output.write("\t%" + str(self._current_reg) + " = alloca " + memory_type + ", align " + str(size) + '\n')
        returnval = self._current_reg
        self._regToType[returnval] = memory_type
        self.incrReg()
        return returnval

    def storeInReg(self, value, registernum: int, memory_type: str, size: int):
        # "store i32 1, i32* %1, align 4"
        self._output.write("\t" + "store " + memory_type + ' ' + value
                           + ", " + memory_type + "* %" + str(registernum) +
                           ", align " + str(size) + '\n')

    def incrReg(self):
        self._current_reg += 1

    def loadInRegister(self, memorytype:str, size:int, reg_tocopy: int):

        # %4 = load i32, i32* %1, align 4
        self._output.write("\t%" + str(self._current_reg) + " = load " + memorytype + ", "+memorytype+"* %" + str(reg_tocopy) + ", align " + str(size) + '\n')

        returnval = self._current_reg
        self._regToType[returnval] = memorytype
        self.incrReg()
        return returnval

    def binOp(self, op : str, memorytype: str, v1, v2):
        #   %6 = add nsw i32 %4, %5
        self._output.write("\t%" + str(self._current_reg)+" = "+op +" nsw " + memorytype + str(v1) + ', ' + v2)
        returnval = self._current_reg
        self.incrReg()
        return returnval
