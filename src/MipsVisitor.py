import os

from ASTVisitor import AbsASTVisitor
from Nodes.ArrayNodes import StringNode
from Nodes.Nodes import *


class Register:
    name: str
    number: int
    free: bool
    value: TermNode

    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.free = True


class glob:
    val: str
    name: str

    def __init__(self, val, name):
        self.val = val
        self.name = name

    def getValue(self):
        return self.val


class ASCIIZ(glob):
    @staticmethod
    def getType():
        return 'asciiz'

    def __init__(self, val, name):
        super().__init__(val, name)

    def getValue(self):
        return f'"{self.val}"'

    def __str__(self):
        return f'"{self.val}"'


class FLOAT(glob):
    @staticmethod
    def getType():
        return 'float'

    def __init__(self, val, name):
        super().__init__(val, name)

    def __str__(self):
        return f'{self.val}'


class RegisterTable:
    # dict[str: list[Register]]
    registers: dict

    def __init__(self):
        self.registers = {
            '$zero': [Register('$zero', 0)],
            '$v': [Register(f'$v{v}', v + 2) for v in range(2)],
            '$a': [Register(f'$a{a}', a + 4) for a in range(4)],
            '$t': [Register(f'$t{t}', t + 8) for t in range(8)] + [Register(f't{t + 8}', t + 23) for t in range(2)],
            '$s': [Register(f'$s{s}', s + 16) for s in range(8)],
            '$gp': [Register('$gp', 28)],
            '$sp': [Register('$sp', 29)],
            '$fp': [Register('$fp', 30)],
            '$ra': [Register('$ra', 30)],
            '$f': [Register(f'$f{f}', 32 + f) for f in range(32)]
        }

    def setValue(self, register: str, val: TermNode):
        self.findRegister(register=register).value = val

    def getValue(self, register: str):
        return self.findRegister(register=register).value

    def findRegister(self, register: str):
        if register in ('$zero', '$gp', '$sp', '$fp', '$ra'):
            return self.registers[register][0]
        else:
            return self.registers[register[0:2]][register[2:]]


class MipsInstruction:
    comment = ''

    def setComment(self, comment):
        self.comment = comment

    def __str__(self):
        if self.comment:
            return f'\t#{self.comment}'
        else:
            return ''


class TwoRegInstruction(MipsInstruction):
    lhs: str
    rhs: str
    operation: int

    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.operation = op

    def __str__(self):
        return f'{self.operation}\t{self.lhs}, {self.rhs} {MipsInstruction.__str__(self)}'


class cvt_s_w(TwoRegInstruction):
    def __init__(self, r1, r2):
        super().__init__(r1, r2, 'cvt.s.w')

class TwoRegMemoryInstruction(TwoRegInstruction):
    offset: int  # bytes

    def __init__(self, r1, r2, operation, offset):
        super().__init__(r1, r2, operation)
        self.offset = offset

    def __str__(self):
        return f'{self.operation}\t{self.lhs}, {self.offset}({self.rhs}) {MipsInstruction.__str__(self)}'


class LA(TwoRegMemoryInstruction):
    def __init__(self, r1, r2, offset):
        super().__init__(r1, r2, 'LA', offset)


class OneRegInstruction(MipsInstruction):
    r = ''

    def __init__(self, r, operation):
        self.r = r
        self.operation = operation

    def __str__(self):
        return f'{self.operation}\t{self.r}{super().__str__()}'


class ImmediateInstruction(MipsInstruction):
    r: str
    value: int
    operation: str

    def __init__(self, r, operation, val):
        self.r = r
        self.value = val
        self.operation = operation

    def __str__(self):
        return f'{self.operation}\t{self.r}, {self.value} {super().__str__()}'


class LI(ImmediateInstruction):
    def __init__(self, reg, value):
        if isinstance(value,str):
            value = f"'{value}'"
        super().__init__(reg, 'li', value)


class LWC1(ImmediateInstruction):
    def __init__(self, reg, label):
        super().__init__(reg, 'lwc1', label)
class LWC1Mem(TwoRegMemoryInstruction):
    def __init__(self, reg, reg2, offset):
        super().__init__(r1=reg,r2=reg2, operation='lwc1', offset=offset)


class SW(TwoRegMemoryInstruction):
    def __init__(self, r1, r2, offset):
        super(SW, self).__init__(r1, r2, 'sw', offset)

class SWC1(TwoRegMemoryInstruction):
    def __init__(self, r1, r2, offset):
        super(SWC1, self).__init__(r1, r2, 'swc1', offset)


class StoreReturnAddress(SW):
    def __init__(self):
        super(StoreReturnAddress, self).__init__('$ra', '$fp', -4)


class LW(TwoRegMemoryInstruction):
    def __init__(self, r1, r2, offset):
        super(LW, self).__init__(r1, r2, 'lw', offset)


class LB(TwoRegMemoryInstruction):
    def __init__(self, r1, r2, offset):
        super(LB, self).__init__(r1, r2, 'LB', offset)


class RestoreReturnAddress(LW):
    def __init__(self):
        super(RestoreReturnAddress, self).__init__('$ra', '$fp', -4)


class MOVE(TwoRegInstruction):
    def __init__(self, r1, r2):
        super(MOVE, self).__init__(r1, r2, 'move')


class MoveSpToFp(MOVE):
    def __init__(self):
        super(MoveSpToFp, self).__init__('$fp', '$sp')


class MoveFpToSp(MOVE):
    def __init__(self):
        super(MoveFpToSp, self).__init__('$sp', '$fp')


class SaveOldFramePointer(SW):
    def __init__(self):
        super(SaveOldFramePointer, self).__init__('$fp', '$sp', 0)


class RestoreOldFramePointer(LW):
    def __init__(self):
        super(RestoreOldFramePointer, self).__init__('$fp', '$sp', 0)


class J(OneRegInstruction):
    def __init__(self, r1):
        super(J, self).__init__(r1, 'J')


class JR(OneRegInstruction):
    def __init__(self, r1):
        super(JR, self).__init__(r1, 'JR')


class Return(JR):
    def __init__(self):
        super(Return, self).__init__('$ra')


class TwoRegImmInstruction(MipsInstruction):
    r1: str
    r2: str
    v: int
    op: str

    def __init__(self, r1, r2, v, op):
        self.r1 = r1
        self.r2 = r2
        self.v = v
        self.op = op

    def __str__(self):
        return f'{self.op}\t{self.r1}, {self.r2}, {self.v}\t{super().__str__()}'


class SUBU(TwoRegImmInstruction):
    def __init__(self, r1, r2, v):
        super(SUBU, self).__init__(r1, r2, v, 'subu')


class ADDI(TwoRegImmInstruction):
    def __init__(self, r1, r2, v):
        super(ADDI, self).__init__(r1, r2, v, 'addi')


class ADD(TwoRegImmInstruction):
    def __init__(self, r1, r2, r3):
        super(ADD, self).__init__(r1, r2, r3, 'add')


class AllocateXBytes(SUBU):
    def __init__(self, x):
        super(AllocateXBytes, self).__init__('$sp', '$sp', x)


class JAL(OneRegInstruction):
    def __init__(self, label):
        super(JAL, self).__init__(operation='JAL', r=label)


class LALab(MipsInstruction):
    r1: str
    label: str

    def __init__(self, r1, label):
        super().__init__()
        self.r1 = r1
        self.label = label

    def __str__(self):
        return f'LA {self.r1}, {self.label}'


class MipsBuilder:
    pass


class MipsBlock:
    name: str
    # list[MipsInstruction]
    Instructions: list
    is_terminated: bool

    def __init__(self, name):
        self.name = name
        self.Instructions = []
        self.is_terminated = False

    def branch(self, blockLabel: str, comm):
        self.is_terminated = True
        ins = J(blockLabel)
        ins.comment = comm
        self.addInstruction(ins)


    def addInstruction(self, instruction: MipsInstruction):
        self.Instructions.append(instruction)

    def __str__(self):
        out = f'{self.name}:\n'
        for instruction in self.Instructions:
            out += f'\t{str(instruction)}\n'
        return out + '\n'


# class Main(MipsBlock):
# def __init__(self):
# super().__init__('main')
# self.addInstruction(LA())
class Exit(MipsBlock):
    def __init__(self):
        super().__init__('exit')
        self.addInstruction(LI('$v0', 10))
        self.addInstruction(SystCall())


class MipsModule:
    # dict[name:glob]
    globals = dict
    Functions = list
    main: MipsBlock
    exit: MipsBlock

    def __init__(self):
        self.Functions = []
        self.globals = {}
        # self.main = Main()
        self.exit = Exit()
        self.main = None

    def addGlobal(self, glob, index=0):
        n = f'{glob.name}_{index}'
        if n in self.globals:
            return self.addGlobal(glob, index + 1)
        else:
            glob.name = n
            self.globals[n] = glob
            return n

    def addFunction(self, func):
        if func.name == 'main':
            self.main = func
        else:
            self.Functions.append(func)

    def __str__(self):
        out = f'.globl main' \
              f'\n########################################################################\n\n'

        out += '.data\n'
        for identifier, glob in self.globals.items():
            out += f'\t{identifier}: .{glob.getType()} {glob.getValue()}\n'

        out += '\n.text\n'
        for funct in self.Functions:
            out += f'{funct.__str__()}\n'

        out += f'{self.main.__str__()}'
        out += f'{self.exit.__str__()}'

        return out


class StackAllocation(MipsBlock):

    def __init__(self, nr_regs, name):
        super().__init__(f'{name}_StackAllocation')
        self.setNrRegs(nr_regs)

    def setNrRegs(self, wordsToAllocate):
        self.Instructions = []
        temp = MipsInstruction()
        temp.setComment('Allocate Stack Recources')
        self.addInstruction(temp)
        self.addInstruction(SaveOldFramePointer())
        self.addInstruction(MoveSpToFp())

        self.addInstruction(AllocateXBytes(4 * wordsToAllocate + 8))
        self.addInstruction(StoreReturnAddress())
        temp = MipsInstruction()
        temp.setComment('Start function')
        self.addInstruction(temp)

        # for reg in range(0, nr_regs):
        #     self.addInstruction(SW(f'$s{reg}', f'$fp', -4 * reg - 8))


class StackRestoration(MipsBlock):
    def __init__(self, name):
        super().__init__(f'{name}_Exit')
        self.Instructions = []
        temp = MipsInstruction()
        temp.setComment('Restore Stack Recources')
        self.addInstruction(temp)
        # for reg in range(nr_regs - 1, -1, -1):
        #     self.addInstruction(LW(f'$s{reg}', f'$fp', -4 * reg - 8))

        self.addInstruction(RestoreReturnAddress())
        self.addInstruction(MoveFpToSp())
        self.addInstruction(RestoreOldFramePointer())
        if name != 'main':
            self.addInstruction(Return())

class MemoryLocation:
    base: str
    offset: int

    def __init__(self, base, offset):
        self.base = base
        self.offset = offset

    def __str__(self):
        return f'{self.offset}({self.base})'


class MipsFunction:
    # list[MipsBlock]
    blocks: list
    name: str
    memoryptr: int

    def __init__(self, name, size):
        self.blocks = []
        self.blocks.append(StackAllocation(name=name, nr_regs=size))
        self.blocks.append(StackRestoration(name=name))

        self.name = name
        self.size = size

    def append_basic_block(self, block):
        self.blocks.insert(len(self.blocks) - 1, block)
        return block

    def __str__(self):
        out = f'{self.name}:\n'
        # out += f'#Allocate Stack Recources'
        # for i in range(self.size//4):
        #
        # out += f'#FUNCTION'
        for block in self.blocks:
            out += block.__str__()
        # out += f'#Return Stack Recources'
        # out += f'{self.name}-exit'
        return out


def GrabArgs(arguments, MipsBlock):
    if arguments:
        i = MipsInstruction()
        i.comment = 'Grab the arguments'

    for argument in range(arguments):
        MipsBlock.addInstruction(MOVE(f'$s{argument}', f'$a{argument}'))


class BEQ(MipsInstruction):
    r1: str
    r2: str
    branch_label: str

    def __init__(self, r1, r2, branch_label):
        self.r1 = r1
        self.r2 = r2
        self.branch_label = branch_label

    def __str__(self):
        return f'beq\t{self.r1}, {self.r2}, {self.branch_label}'


class SystCall(MipsInstruction):
    def __str__(self):
        return 'SYSCALL'


class MipsPrintF(MipsFunction):
    def __init__(self):
        super().__init__(name='printf', size=6)
        GrabArgs(3, self.blocks[0])
        buffer = MipsBlock('printf_buffer')
        i = LA('$t0', '$s0', 0)
        i.setComment('t0 is current start of string')
        buffer.addInstruction(i)
        i = ADDI('$t1', '$sp', 16)
        i.setComment('t1 is the current argument')
        buffer.addInstruction(i)

        loop = MipsBlock('printf_loop')
        loop.addInstruction(LB('$a0', '$t0', 0))
        loop.addInstruction(BEQ('$a0', '$zero', 'printf_Exit'))
        loop.addInstruction(ADDI('$t0', '$t0', 1))

        printf_char = MipsBlock('printf_char')

        i = LI('$v0', 11)
        i.setComment('argument for character print')
        printf_char.addInstruction(i)

        i = SystCall()
        i.comment = 'Print the character'
        printf_char.addInstruction(i)

        printf_char.addInstruction(J('printf_loop'))

        self.append_basic_block(buffer)
        self.append_basic_block(loop)
        self.append_basic_block(printf_char)


class ThreeRegInstruction(MipsInstruction):
    r1: str
    r2: str
    r3: str
    op: str

    def __init__(self, r1, r2, r3, op):
        self.r3 = r3
        self.r2 = r2
        self.r1 = r1
        self.op = op

    def __str__(self):
        return f'{self.op} {self.r1}, {self.r2}, {self.r3}'


class Cmp(ThreeRegInstruction):
    def __init__(self, r1, r2, r3, op):
        if op == '<':
            op = 'slt'
        elif op == '>=':
            op = 'sge'
        elif op == '==':
            op = 'seq'
        elif op == '!=':
            op = 'sne'
        else:
            raise Exception
        super().__init__(r1, r2, r3, op)


class AND(ThreeRegInstruction):
    def __init__(self, r1, r2, r3):
        super().__init__(r1, r2, r3, op='and')


class BNE(ThreeRegInstruction):
    def __init__(self, r1, r2, truebr):
        if r1 is None:
            raise Exception
        super().__init__(r1=r1, r2=r2, r3=truebr, op='bne')



class MipsVisitor(AbsASTVisitor):
    module: MipsModule
    builder: MipsBuilder
    current_function: MipsFunction
    globals: list
    _symbol_table = None
    printf = MipsPrintF()
    registers = RegisterTable()
    continueBlock: MipsBlock
    breakBlock: MipsBlock

    def __init__(self, ctx: CodeblockNode, filepath: str, run=False):
        self.globals = []
        self.builder = None
        self.module = MipsModule()
        self.module.addFunction(self.printf)
        self.current_function = None
        # a = StackAllocation(4, 'main')
        # print(a)
        # print(StackRestoration(4, 'main'))
        try:
            # self._output = open(file=filepath, mode='w')

            # self.current_function = None
            # # Now implement the function
            #
            super().__init__(ctx)
            # self.block.ret(ir.Constant(i32, 0))


        except Exception as e:

            raise e
        finally:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            _output = open(file=filepath, mode='w+')
            _output.write(str(self.module))
            # self._output.write(str(self.module))
            # self._output.close()
    def visitWhilestatementNode(self, ctx: WhilestatementNode):
        self.pushSymbolTable(ctx.symbol_table)

        cond_block: MipsBlock = MipsBlock(name=f'while_condition_line{ctx.getMetaData().getLine()}')

        while_block: MipsBlock = MipsBlock(name=f'while_line{ctx.getMetaData().getLine()}')

        elihw_block: MipsBlock = MipsBlock(name=f'elihw_line{ctx.getMetaData().getLine()}')


        self.continueBlock = cond_block
        self.breakBlock = elihw_block

        self.breakBlock = elihw_block
        self.continueBlock = cond_block
        if not self.block.is_terminated:
            self.block.branch(cond_block.name, "Check while condition")
        self.block = cond_block
        self.current_function.append_basic_block(cond_block)

        condition = self.visit(ctx.condition)
        # if condition.type == i32:
        #     condition = self.block.icmp_signed("!=", condition, ir.Constant(i32, 0))
        self.block.addInstruction(BNE(r1=condition, r2='$zero', truebr=while_block.name))
        self.block.addInstruction(J(elihw_block.name))

        self.current_function.append_basic_block(while_block)
        self.block = while_block
        self.visitCodeBlockNode(ctx.block)
        if not self.block.is_terminated:
            self.block.branch(cond_block.name, "check while condition")

        self.current_function.append_basic_block(elihw_block)
        self.block = elihw_block
        self.popSymbolTable()

        self.continueBlock = None
        self.breakBlock = None

        return



    def default(self, ctx: AbsNode):
        for child in ctx.getChildren():
            self.visit(child)

    def visitFunctionDefinition(self, ctx: FunctionDefinition):

        self.pushSymbolTable(ctx.symbol_table)

        self.current_function = MipsFunction(name=ctx.functionName, size=ctx.spaceToAllocate())
        self.module.addFunction(self.current_function)
        newblock = MipsBlock(f"function_start_{ctx.getName()}")
        self.block = self.current_function.append_basic_block(newblock)

        returnblock = MipsBlock(name=f"{ctx.getName()}_Exit")
        self.current_function.return_block = returnblock


        # for variable in self.globals:
        #     a: ir.AllocaInstr = self.block.alloca(variable.type, 1, variable.name)
        #

        s = -4
        for variable in self._symbol_table.variables.values():
            varnode: VariableNode = variable.node
            # a: ir.AllocaInstr = self.block.alloca(varnode.getLLVMType(), 1, varnode.getName())
            s -= 4
            reg = s
            variable.register = reg
        self.current_function.memoryptr = s

        self.default(ctx)
        # if ctx.getName() == 'main' and not self.block.is_terminated:
        #     self.block.ret(ir.Constant(i32, 1))
        # elif ctx.returntype == 'void' and not self.block.is_terminated:
        #     self.block.ret_void()
        # else:
        #     result = self.load(self.current_function.return_address)
        #     self.block.ret(result)
        self.popSymbolTable()

    def visitBreakNode(self, ctx: BreakNode):
        self.block.branch(self.breakBlock.name, "Break")

    def visitContinueNode(self, ctx: ContinueNode):

        self.block.branch(self.continueBlock.name, "Continue")

    def visitFunctionBody(self, ctx: FunctionBody):

        return self.default(ctx)

    def visitCodeBlockNode(self, ctx: CodeblockNode):
        ctx.symbol_table.parent = self._symbol_table
        self._symbol_table = ctx.symbol_table

        if self.current_function:
            for variable in self._symbol_table.variables.values():
                varnode: VariableNode = variable.node
                a: ir.AllocaInstr = self.block.alloca(varnode.getLLVMType(), 1, varnode.getName())
                variable.register = a

        self.default(ctx)

        self._symbol_table = ctx.symbol_table.parent

    def visitTermNode(self, ctx: TermNode):
        return ctx.value

    def visitUnOpNode(self, ctx: UnOpNode):
        pass

    def visitReturnNode(self, ctx: ReturnNode):
        value = self.visit(ctx.child)
        if value is not None:
            self.block.addInstruction(LI('$v0', value))
        ret_blo = self.current_function.return_block
        self.block.branch(ret_blo.name, "function return")
        return

    def visitVariableNameNode(self, ctx: VariableNameNode):
        lookasigned = ctx.rvalue
        table_entry: VariableEntry = self._symbol_table.getTableEntry(ctx.getName(), lookasigned)
        ins = table_entry.register
        return MemoryLocation('$sp', ins)

    def visitVariableIntNode(self, ctx: VariableIntNode):
        return self.visitVariableNode(ctx)

    def visitVariableCharNode(self, ctx: VariableCharNode):
        return self.visitVariableNode(ctx)

    def visitVariableFloatNode(self, ctx: VariableFloatNode):
        return self.visitVariableNode(ctx)

    def visitVariableNode(self, ctx: VariableNode):
        return self.visitVariableNameNode(ctx)

    def visitFunctionNode(self, ctx: FunctionNode):
        fmt_args = self.visit(ctx.argumentNode)
        for arg_ind in range(len(fmt_args)):
            LI(f'$a{arg_ind}',fmt_args[arg_ind])

        return self.block.addInstruction(JAL(ctx.functionName))

    def callprintf(self, str):
        identifier = self.module.addGlobal(ASCIIZ(name=f'str', val=str))
        self.block.addInstruction(LALab('$a0', f'{identifier}'))
        self.block.addInstruction(JAL('printf'))

    def visitPrintfNode(self, ctx: PrintfNode):
        fmt_args = self.visit(ctx.argumentNode)
        processing: str = fmt_args[0]
        identifier: str
        processing = ('%r' % processing)[1:-1]
        # processing = re.sub(r'\\', r'a', processing)
        # processing= processing.encode('UTF-8').replace('\\','\\\\')
        # processing= processing.decode('ascii')
        temp: list[str]
        str_ind = 0
        for arg_ind in range(1, len(fmt_args)):
            str_ind = processing.find('%', str_ind, len(processing) + 1)
            if processing[str_ind + 1] == 'd':
                temp = processing.split("%d", 1)
                self.callprintf(temp[0])

                if isinstance(fmt_args[arg_ind], int):
                    self.block.addInstruction(LI('$a0', fmt_args[arg_ind]))
                else:
                    self.block.addInstruction(LW('$a0', fmt_args[arg_ind].base, fmt_args[arg_ind].offset))
                self.block.addInstruction(LI('$v0', 1))
            elif processing[str_ind + 1] == 'c':
                temp = processing.split("%c", 1)
                self.callprintf(temp[0])

                if isinstance(fmt_args[arg_ind], str) and len(fmt_args[arg_ind]) == 1:
                    self.block.addInstruction(LI('$a0', '%r' % fmt_args[arg_ind]))
                else:
                    self.block.addInstruction(LW('$a0', fmt_args[arg_ind].base, fmt_args[arg_ind].offset))
                self.block.addInstruction(LI('$v0', 11))
            elif processing[str_ind + 1] == 'f':
                temp = processing.split("%f", 1)
                self.callprintf(temp[0])
                if isinstance(fmt_args[arg_ind], float):
                    label = self.module.addGlobal(FLOAT(name=f'float', val=fmt_args[arg_ind]))
                    self.block.addInstruction(LWC1('$f12', label))
                else:
                    self.block.addInstruction(LWC1Mem('$f12', fmt_args[arg_ind].base, fmt_args[arg_ind].offset))
                self.block.addInstruction(LI('$v0', 2))
            else:
                continue
            self.block.addInstruction(SystCall())
            processing = temp[1]
        identifier = self.module.addGlobal(ASCIIZ(name='str', val=processing))
        self.block.addInstruction(LALab('$a0', identifier))
        self.block.addInstruction(JAL('printf'))
        return

    def visitArgumentNode(self, ctx: ArgumentsNode):
        arguments: list = []
        for arg in ctx.getChildren():
            arguments.append(self.visit(arg))
        return arguments

    def visitRefNode(self, ctx: RefNode):
        a: ir.Instruction = self._symbol_table.getTableEntry(ctx.child.getName()).register

        return a

    def visitIfElsestatementNode(self, ctx: IfElseStatementNode):
        self.pushSymbolTable(ctx.symbol_table)

        condition = self.visit(ctx.condition)

        if_block = MipsBlock(f"if_line_{ctx.getMetaData().getLine()}")
        elseif_block = MipsBlock(f"else_line_{ctx.getMetaData().getLine()}")
        endif_block = MipsBlock(f"endif_line_{ctx.getMetaData().getStopLine()}")

        self.block.addInstruction(BNE(r1=condition, r2='$zero', truebr=if_block.name))
        self.block.branch(elseif_block.name, "go to else block")

        self.current_function.append_basic_block(if_block)
        self.block = if_block
        self.visitCodeBlockNode(ctx.block)
        if not self.block.is_terminated:
            self.block.branch(endif_block.name, "go to end of if statement")

        self.current_function.append_basic_block(elseif_block)
        self.block = elseif_block
        self.visitCodeBlockNode(ctx.else_statement.block)

        if not self.block.is_terminated:
            self.block.branch(endif_block.name, "go to end of if statement")

        self.current_function.append_basic_block(endif_block)
        self.block = endif_block

        self.popSymbolTable()

    def visitIfstatementNode(self, ctx: IfstatementNode):
        self.pushSymbolTable(ctx.symbol_table)
        condition = self.visit(ctx.condition)

        if_block = MipsBlock(f"if_line_{ctx.getMetaData().getLine()}")
        self.current_function.append_basic_block(if_block)
        endif_block = MipsBlock(f"endif_line_{ctx.getMetaData().getStopLine()}")

        self.block.addInstruction(BNE(r1=condition, r2='$zero', truebr=if_block.name))
        self.block.addInstruction(J(endif_block.name))
        # self.block.cbranch(cond=condition, truebr=if_block, falsebr=endif_block)

        self.block = if_block
        self.visitCodeBlockNode(ctx.block)
        self.block.addInstruction(J(endif_block.name))

        endif_block = self.current_function.append_basic_block(endif_block)
        self.block = endif_block
        self.popSymbolTable()

        return

    def visitAssNode(self, ctx: AssNode):
        node: VariableEntry = self._symbol_table.getTableEntry(ctx.lhs.getName())
        value: MemoryLocation
        # todo
        if not self.current_function:
            gv = ir.GlobalVariable(module=self.module, name=ctx.lhs.getName(), typ=ctx.rhs.getLLVMType())
            gv.initializer = ctx.rhs.llvmValue()
            self._symbol_table.getTableEntry(ctx.lhs.getName()).register = gv
            self.globals.append(gv)
            return
        returnReg:str
        if isinstance(ctx.rhs, TermNode):
            node.stored_value = ctx.rhs.value
            if isinstance(ctx.rhs,TermFloatNode):
                returnReg = '$f0'
                label = self.module.addGlobal(FLOAT(name=f'float', val=node.stored_value))
                self.block.addInstruction(LWC1(returnReg, label))
                self.block.addInstruction(SWC1(r1=returnReg, r2='$sp', offset=node.register))

            else:
                returnReg = '$t0'
                self.block.addInstruction(LI(value=node.stored_value, reg=returnReg))
                self.block.addInstruction(SW(r1=returnReg, r2='$sp', offset=node.register))
            return returnReg
        value = self.visit(ctx.rhs)
        lhs = self.visit(ctx.lhs)


        # value = self.convertTo(value, ctx)
        node.stored_value = value

        if ctx.lhs.getType() == 'float':
            if isinstance(value, MemoryLocation) and not isinstance(ctx.rhs, RefNode):
                self.block.addInstruction(LWC1Mem('$f0', value.base, value.offset))
            if ctx.rhs.getType() == 'i32':
                self.block.addInstruction(cvt_s_w(r1='$f0',r2='$f0'))

            returnReg = '$f0'
            # self.block.addInstruction(LWC1Mem(returnReg, lhs.base,lhs.offset ))
            self.block.addInstruction(SWC1(r1=returnReg, r2='$sp', offset=node.register))
            return returnReg
        else:
            if isinstance(value, MemoryLocation) and not isinstance(ctx.rhs, RefNode):
                self.block.addInstruction(LW('$t0', value.base, value.offset))
            self.block.addInstruction(SW('$t0',lhs.base,lhs.offset))
            return '$t0'

        return '$t0'

    def load(self, ins: MemoryLocation):
        if not isinstance(ins, MemoryLocation):
                # and not isinstance(ins, ir.GlobalVariable) and not isinstance(ins, ir.GEPInstr):
            return ins
        else:
            # name = ins.base
            self.block.addInstruction(LW('$t0',ins.base,ins.offset))
            return '$t0'

    def visitPointerNode(self, ctx: PointerNode):
        if ctx.getChildren()[0] and isinstance(ctx._child, StringNode):
            return self.visit(ctx.getChildren()[0])
        reg: ir.Instruction = self._symbol_table.getTableEntry(ctx.getName()).register
        while reg.type.is_pointer:
            reg = self.block.load(reg, name=reg.name)
        return reg

    def visitStringNode(self, ctx: StringNode):
        fmt = f'{ctx.getFullString()}'
        return fmt

    def visitBinOpNode(self, ctx: BinOpNode):
        v1: MemoryLocation = self.visit(ctx.lhs)
        v2 = self.visit(ctx.rhs)

        # copy and load to new reg
        for reg in ((v1,'$t0'),(v2,'$t1')):
            if isinstance(reg[0],MemoryLocation):
                self.block.addInstruction(LW(reg[1], reg[0].base, reg[0].offset))
            else:
                self.block.addInstruction(LI(reg[1], reg[0]))

        return '$t0', '$t1'

    def visitBinPlusNode(self, ctx: BinPlusNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)

        # integer addition
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.block.addInstruction(ADD(v1, v1, v2))
        # fp addition
        return self.block.fadd(v1, v2)

    def visitBinLTENode(self, ctx: BinLTENode):
        super().visitBinLTENode(ctx)

    def visitBinAndNode(self, ctx: BinAndNode):
        self.current_function.memoryptr -= 4
        v1: str = self.visit(ctx.lhs)
        self.block.addInstruction(SW(v1, '$sp', self.current_function.memoryptr))

        v2 = self.visit(ctx.rhs)

        if isinstance(v2, int):
            self.block.addInstruction(Cmp(r1='$t0', r2='$t1', op="!=", r3='$t0'))
        self.block.addInstruction(MOVE('$t1', '$t0'))
        self.block.addInstruction(LW('$t0', '$sp', self.current_function.memoryptr))

        self.current_function.memoryptr += 4
        self.block.addInstruction(AND('$t0', '$t0', '$t1'))
        return '$t0'
        # c1 = self.main.sitofp(v1,cbool)
        # c2 = self.main.sitofp(v2,cbool)
        # self.main.zext(c1,i32)
        # voidptr_ty = cchar.as_pointer()
        # fmt = "%d ~~; \00"
        # c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
        #                     bytearray(fmt.encode("utf8")))
        # global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=str(id(ctx)))
        # global_fmt.global_constant = True
        # global_fmt.initializer = c_fmt
        # a = self.main.bitcast(global_fmt, voidptr_ty, "str")
        # fmt_args = [a, c1]
        # self.main.call(self.printf, fmt_args)

    def visitBinOrNode(self, ctx: BinOrNode):
        super().visitBinOrNode(ctx)

    def visitBinEQNode(self, ctx: BinEQNode):
        return self.compOp(ctx, op='==')

    def visitBinModNode(self, ctx: BinModNode):
        super().visitBinModNode(ctx)

    def visitBinDisNode(self, ctx: BinDisNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)
        # integer multiplication
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.block.sdiv(v1, v2)
        # fp multiplication
        return self.block.fdiv(v1, v2)

    def visitBinMinNode(self, ctx: BinMinNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)
        # integer multiplication
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.block.sub(v1, v2)
        # fp multiplication
        return self.block.fsub(v1, v2)

    def visitBinGTNode(self, ctx: BinGTNode):
        super().visitBinGTNode(ctx)

    def compOp(self, ctx: BinOpNode, op):
        lhs = self.visit(ctx.lhs)
        rhs = self.visit(ctx.rhs)
        if isinstance(lhs, MemoryLocation):
            self.block.addInstruction(LW('$t0', lhs.base, lhs.offset))
        else:
            self.block.addInstruction(LI('$t0', lhs))
        if isinstance(rhs, MemoryLocation):
            self.block.addInstruction(LW('$t1', rhs.base, rhs.offset))
        else:
            self.block.addInstruction(LI('$t1', rhs))
        self.block.addInstruction(Cmp(r1='$t0', r2='$t0', r3='$t1', op=f'{op}'))
        return '$t0'

    def visitBinGTENode(self, ctx: BinGTENode):
        return self.compOp(ctx, '>=')

    def visitBinNENode(self, ctx: BinNENode):
        return self.compOp(ctx, '!=')

    def visitBinMulNode(self, ctx: BinMulNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)
        # integer multiplication
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.block.mul(v1, v2)
        # fp multiplication
        return self.block.fmul(v1, v2)

    def visitBinLTNode(self, ctx: BinLTNode):

        return self.compOp(ctx, '<')

    def convertTo(self, value, ctx):
        if ctx.getLLVMType() != value.type:
            if ctx.getLLVMType() == cfloat and value.type == i32:
                return self.block.sitofp(value, ctx.getLLVMType())
            if ctx.getLLVMType() == i32 and value.type == cfloat:
                return self.block.fptosi(value, ctx.getLLVMType())
        return value
