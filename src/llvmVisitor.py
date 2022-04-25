from __future__ import print_function
import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE
from llvmbuilder import LLVMBuilder
from ASTVisitor import AbsASTVisitor
from SymbolTable import *
from Nodes import *

fnty = ir.FunctionType(i32, ())


class llvmVisitor(AbsASTVisitor):
    builder: LLVMBuilder
    main: ir.IRBuilder
    module: ir.Module


    def __init__(self, ctx: CodeblockNode, symbol_table: SymbolTable, filepath: str, run=False):
        self.printf: ir.Function = None
        try:
            self._output = open(file=filepath, mode='w')

            # Create an empty module...
            self.module = ir.Module(name="Output.llvm")
            self.module.triple = "x86_64-pc-linux-gnu"

            # and declare a function named "main" inside it
            mainfn = ir.Function(self.module, fnty, name="main")
            # Now implement the function
            block = mainfn.append_basic_block(name="main-entry")
            self.main = ir.IRBuilder(block)

            self.builder = LLVMBuilder(filepath=filepath)
            super().__init__(ctx, symbol_table)

            self._output.write(str(self.module))
            self._output.close()

        except Exception as e:
            self._output.write(str(self.module))
            self._output.close()

            raise e
        if run:
            self.runLLVM()

    def default(self, ctx: AbsNode):
        for child in ctx.getChildren():
            self.visit(child)

    def visitCodeBlockNode(self, ctx: CodeblockNode):
        for variable in self._symbol_table.variables.values():
            varnode: VariableNode = variable.node
            a: ir.AllocaInstr = self.main.alloca(varnode.getLLVMType(), 1, varnode.getName())
            variable.register = a

        self.default(ctx)
        self.main.ret(ir.Constant(i32, 0))

    def visitTermNode(self, ctx: TermNode):
        return ctx.llvmValue()

    def visitUnOpNode(self, ctx: UnOpNode):
        pass

    def visitVariableNameNode(self, ctx: VariableNameNode):
        table_entry: VariableEntry = self._symbol_table.getTableEntry(ctx.getName())
        ins : ir.Instruction = table_entry.register
        return self.main.load(ins,ins.name)

    def visitVariableIntNode(self, ctx: VariableIntNode):
        return self.visitVariableNode(ctx)

    def visitVariableCharNode(self, ctx: VariableCharNode):
        return self.visitVariableNode(ctx)

    def visitVariableFloatNode(self, ctx: VariableFloatNode):
        return self.visitVariableNode(ctx)

    def visitVariableNode(self, ctx: VariableNode):
        return self.visitVariableNameNode(ctx)

    def visitFunctionNode(self, ctx: FunctionNode):
        pass

    def visitPrintfNode(self, ctx: PrintfNode):
        voidptr_ty = cchar.as_pointer()
        if not self.printf:
            printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
            self.printf = ir.Function(self.module, printf_ty, name="printf")
        fmt_args = self.visit(ctx.argumentNode)
        for index in range(1, len(fmt_args)):
            if hasattr(fmt_args[index].type, "pointee") and cchar == fmt_args[index].type.pointee:
                loaded = self.main.load(fmt_args[index], fmt_args[index].name)

                casted = self.main.sext(loaded,i32,name=loaded.name)
                fmt_args[index] = casted
        return self.main.call(self.printf, fmt_args)


    def visitArgumentNode(self, ctx: ArgumentsNode):
        arguments:list = []
        for arg in ctx.getChildren():
            arguments.append(self.visit(arg))
        return arguments

    def visitRefNode(self, ctx: RefNode):
        pass

    def visitAssNode(self, ctx: AssNode):
        node: VariableEntry = self._symbol_table.getTableEntry(ctx.lhs.getName())
        value: ir.Instruction

        if isinstance(ctx.rhs, TermNode):
            return self.main.store(value=node.value.llvmValue(), ptr=node.register)
        value = self.visit(ctx.rhs)
        if value.type.is_pointer:
            value = self.main.load(value,value.name)

        value = self.convertTo(value, ctx)
        return self.main.store(value, node.register)

    def visitPointerNode(self, ctx: PointerNode):
        if ctx.getChildren()[0]:
            return self.visit(ctx.getChildren()[0])

    def visitStringNode(self, ctx: StringNode):

        voidptr_ty = cchar.as_pointer()
        fmt = ctx.getFullString() + "\00"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=str(id(ctx)))
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        return self.main.bitcast(global_fmt, voidptr_ty)

    def visitBinOpNode(self, ctx: BinOpNode):
        v1: ir.Instruction = self.visit(ctx.lhs)
        v2 = self.visit(ctx.rhs)

        # copy and load to new reg
        if v1.type.is_pointer:
            v1 = self.main.load(v1,v1.name)
        if v2.type.is_pointer:
            v2 = self.main.load(v2)

        if ctx.getLLVMType() != v1.type:
            v1 = self.main.sitofp(v1, ctx.getLLVMType())
        if ctx.getLLVMType() != v2.type:
            v2 = self.main.sitofp(v2, ctx.getLLVMType())

        return v1, v2

    def visitBinPlusNode(self, ctx: BinPlusNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)

        # integer addition
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.main.add(v1, v2)
        # fp addition
        return self.main.fadd(v1, v2)

    def visitBinLTENode(self, ctx: BinLTENode):
        super().visitBinLTENode(ctx)

    def visitBinAndNode(self, ctx: BinAndNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)

        c1 = self.main.icmp_signed("==",v1,ir.Constant(i32,0))
        c2 = self.main.icmp_signed("==",v2,ir.Constant(i32,0))
        # c1 = self.main.sitofp(v1,cbool)
        # c2 = self.main.sitofp(v2,cbool)
        # self.main.zext(c1,i32)
        voidptr_ty = cchar.as_pointer()
        fmt = "%d ~~; \00"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=str(id(ctx)))
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        a = self.main.bitcast(global_fmt, voidptr_ty, "str")
        fmt_args = [a, c1]
        self.main.call(self.printf, fmt_args)
        return self.main.and_(c1, c2)


    def visitBinOrNode(self, ctx: BinOrNode):
        super().visitBinOrNode(ctx)

    def visitBinEQNode(self, ctx: BinEQNode):
        super().visitBinEQNode(ctx)

    def visitBinModNode(self, ctx: BinModNode):
        super().visitBinModNode(ctx)

    def visitBinDisNode(self, ctx: BinDisNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)
        # integer multiplication
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.main.sdiv(v1, v2)
        # fp multiplication
        return self.main.fdiv(v1, v2)

    def visitBinMinNode(self, ctx: BinMinNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)
        # integer multiplication
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.main.sub(v1, v2)
        # fp multiplication
        return self.main.fsub(v1, v2)

    def visitBinGTNode(self, ctx: BinGTNode):
        super().visitBinGTNode(ctx)

    def visitBinGTENode(self, ctx: BinGTENode):
        super().visitBinGTENode(ctx)

    def visitBinNENode(self, ctx: BinNENode):
        super().visitBinNENode(ctx)

    def visitBinMulNode(self, ctx: BinMulNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)
        # integer multiplication
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.main.mul(v1, v2)
        # fp multiplication
        return self.main.fmul(v1, v2)

    def visitBinLTNode(self, ctx: BinLTNode):
        super().visitBinLTNode(ctx)

    def runLLVM(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        llvm_module = llvm.parse_assembly(str(self.module))
        tm = llvm.Target.from_default_triple().create_target_machine()

        with llvm.create_mcjit_compiler(llvm_module, tm) as ee:
            ee.finalize_object()
            fptr = ee.get_function_address("main")
            py_func = CFUNCTYPE(None)(fptr)
            py_func()

    def convertTo(self, value, ctx):
        if ctx.getLLVMType() != value.type:
            if ctx.getLLVMType() == cfloat and value.type == i32:
                return self.main.sitofp(value, ctx.getLLVMType())
            if ctx.getLLVMType() == i32 and value.type == cfloat:
                return self.main.fptosi(value, ctx.getLLVMType())
        return value