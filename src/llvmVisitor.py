from __future__ import print_function

import llvmlite.ir
from llvmlite import ir
from llvmbuilder import LLVMBuilder
from ASTVisitor import AbsASTVisitor
from SymbolTable import *
from Nodes import *

fnty = ir.FunctionType(i32, ())


class llvmVisitor(AbsASTVisitor):
    builder: LLVMBuilder
    main: ir.IRBuilder

    def __init__(self, ctx, symbol_table, filepath: str):
        # try:
        self._output = open(file=filepath, mode='w')

        # Create an empty module...
        self.module = ir.Module(name="Output.llvm")
        # and declare a function named "main" inside it
        mainfn = ir.Function(self.module, fnty, name="main")
        # Now implement the function
        block = mainfn.append_basic_block(name="main-entry")
        self.main = ir.IRBuilder(block)

        self.builder = LLVMBuilder(filepath=filepath)
        super().__init__(ctx, symbol_table)

        self._output.write(str(self.module))
        self._output.close()

    # except Exception as e:
    # self._output.write(str(self.module))
    # self._output.close()

    # raise e

    def default(self, ctx):
        for child in ctx.getChildren():
            self.visit(child)

    def visitCodeBlockNode(self, ctx: CodeblockNode):
        for variable in self._symbol_table.variables.values():
            a: ir.AllocaInstr = self.main.alloca(variable.node.getLLVMType(), 1)
            variable.register = a

            # variable.register = self.builder.allocateMemory(variable.node.getType(), variable.node.getSize())

        self.default(ctx)
        self.main.ret(ir.Constant(i32, 0))

    def visitTermNode(self, ctx: TermNode):
        return ctx.llvmValue()

    def visitUnOpNode(self, ctx: UnOpNode):
        pass

    def visitVariableNameNode(self, ctx: VariableNameNode):
        table_entry: VariableEntry = self._symbol_table.getTableEntry(ctx.getName())
        node: VariableNode = table_entry.node
        memtype = node.getType()
        size = node.getSize()
        reg_tocopy = table_entry.register

        # return '%' + str(self.builder.loadInRegister(memorytype=memtype, size=size, reg_tocopy=reg_tocopy))
        return table_entry.register

    def visitVariableIntNode(self, ctx: VariableIntNode):
        return self.visitVariableNode(ctx)

    def visitVariableCharNode(self, ctx):
        return self.visitVariableNode(ctx)

    def visitVariableFloatNode(self, ctx):
        return self.visitVariableNode(ctx)

    def visitVariableNode(self, ctx: VariableNode):
        return self.visitVariableNameNode(ctx)

    def visitFunctionNode(self, ctx: FunctionNode):
        pass

    def visitPrintfNode(self, ctx: PrintfNode):
        pass

    def visitRefNode(self, ctx: RefNode):
        pass

    def visitAssNode(self, ctx: AssNode):
        node: VariableEntry = self._symbol_table.getTableEntry(ctx.lhs.getName())
        value: ir.Instruction

        if isinstance(ctx.rhs, TermNode):
            # value = node.value
            return self.main.store(value=ir.Constant(node.node.getLLVMType(), node.value), ptr=node.register)
        value = self.visit(ctx.rhs)
        if ctx.lhs.getLLVMType() != value.type:
            value = self.main.sitofp(value, ctx.lhs.getLLVMType())
        self.main.store(value, node.register)
        # self.builder.storeInReg(value=value, registernum=node.register, memory_type=node.node.getType(),
        #                         size=node.node.getSize())

    def visitPointerNode(self, ctx: PointerNode):
        pass

    def visitBinOpNode(self, ctx: BinOpNode):
        v1: ir.Instruction = self.visit(ctx.lhs)
        v2 = self.visit(ctx.rhs)

        # copy and load to new reg
        if v1.type.is_pointer:
            v1 = self.main.load(v1)
        if v2.type.is_pointer:
            v2 = self.main.load(v2)
        return v1, v2

    def visitBinPlusNode(self, ctx: BinPlusNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)

        # integer addition
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.main.add(v1, v2)
        # fp addition
        return self.main.fadd(v1, v2)

    def visitBinLTENode(self, ctx):
        super().visitBinLTENode(ctx)

    def visitBinAndNode(self, ctx):
        super().visitBinAndNode(ctx)

    def visitBinOrNode(self, ctx):
        super().visitBinOrNode(ctx)

    def visitBinEQNode(self, ctx):
        super().visitBinEQNode(ctx)

    def visitBinModNode(self, ctx):
        super().visitBinModNode(ctx)

    def visitBinDisNode(self, ctx):
        v1, v2 = self.visitBinOpNode(ctx=ctx)
        # integer multiplication
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.main.sdiv(v1, v2)
        # fp multiplication
        return self.main.fdiv(v1, v2)

    def visitBinMinNode(self, ctx):
        v1, v2 = self.visitBinOpNode(ctx=ctx)
        # integer multiplication
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.main.sub(v1, v2)
        # fp multiplication
        return self.main.fsub(v1, v2)

    def visitBinGTNode(self, ctx):
        super().visitBinGTNode(ctx)

    def visitBinGTENode(self, ctx):
        super().visitBinGTENode(ctx)

    def visitBinNENode(self, ctx):
        super().visitBinNENode(ctx)

    def visitBinMulNode(self, ctx):
        v1, v2 = self.visitBinOpNode(ctx=ctx)
        # integer multiplication
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.main.mul(v1, v2)
        # fp multiplication
        return self.main.fmul(v1, v2)

    def visitBinLTNode(self, ctx):
        super().visitBinLTNode(ctx)
