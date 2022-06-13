from __future__ import print_function

import os
import os.path
from ctypes import CFUNCTYPE

import llvmlite.binding as llvm

from ASTVisitor import *
from llvmTypes import *
from llvmbuilder import LLVMBuilder


class llvmVisitor(AbsASTVisitor):
    builder: LLVMBuilder
    block: ir.IRBuilder
    module: ir.Module
    current_function: ir.Function
    globals: list
    _symbol_table = None
    continueBlock: ir.Block
    breakBlock: ir.Block

    def __init__(self, ctx: CodeblockNode, filepath: str, run=False):
        self.printf: ir.Function = None
        self.scanf: ir.Function = None
        self.globals = []
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            self._output = open(file=filepath, mode='w+')

            # Create an empty module...
            self.module = ir.Module(name="Output.llvm")
            self.module.triple = "x86_64-pc-linux-gnu"

            self.current_function = None
            # Now implement the function

            super().__init__(ctx)

        except Exception as e:
            raise e
        finally:
            self._output.write(str(self.module))
            self._output.close()

        if run:
            self.runLLVM()

    def default(self, ctx: AbsNode):
        for child in ctx.getChildren():
            self.visit(child)

    def llvmType(self, type: str):
        if type == 'void':
            return cvoid
        if type == 'int':
            return i32
        if type == 'char':
            return cchar

    def visitFunctionDefinition(self, ctx: FunctionDefinition):
        param_ty = ctx.getArgumentLLVMTypes()
        fnty = ir.FunctionType(ctx.returntype.getLLVMType(), param_ty)
        self.current_function = ir.Function(self.module, fnty, name=ctx.getName())
        self._symbol_table.getFunction(ctx.getName()).memorylocation = self.current_function
        block = self.current_function.append_basic_block(name=f"main-entry-{ctx.getName()}")
        self.block = ir.IRBuilder(block)

        returnblock = ir.Block(parent=self.current_function, name=f"exit-{ctx.getName()}")
        self.current_function.return_block = returnblock

        self.pushSymbolTable(ctx.symbol_table)
        if ctx.returntype:
            self.current_function.return_address = self.block.alloca(ctx.returntype.getLLVMType(), 1, 'return_add')

        for variable in self.globals:
            a: ir.AllocaInstr = self.block.alloca(variable.type, 1, variable.name)

        for variable in self._symbol_table.variables.values():
            varnode: VariableNode = variable.node
            a: ir.AllocaInstr = self.block.alloca(varnode.getLLVMType(), 1, varnode.getName())
            variable.register = a
        args = self.current_function.args
        index = 0
        for arg in ctx.getArguments().getChildren():
            a = self.visit(arg)
            self.block.store(value=args[index], ptr=a)
            index += 1
        self.default(ctx)

        self.current_function.blocks.append(returnblock)
        if not self.block.block.is_terminated:
            self.block.branch(returnblock)
        self.block = ir.IRBuilder(returnblock)
        if ctx.getName() == 'main' and not self.block.block.is_terminated:
            self.block.ret(ir.Constant(i32, 1))
        elif ctx.returntype == 'void' and not self.block.block.is_terminated:
            self.block.ret_void()
        else:
            result = self.load(self.current_function.return_address)
            self.block.ret(result)

        self.popSymbolTable()

    def visitBreakNode(self, ctx: BreakNode):
        self.block.branch(self.breakBlock)

    def visitContinueNode(self, ctx: ContinueNode):
        self.block.branch(self.continueBlock)

    def visitConditionNode(self, ctx):
        pass

    def visitWhilestatementNode(self, ctx: WhilestatementNode):
        self.pushSymbolTable(ctx.symbol_table)
        cond_block = self.block.function.append_basic_block(name='while_condition')
        while_block = self.block.function.append_basic_block(name='while')
        elihw_block = self.block.function.append_basic_block(name='elihw')

        self.continueBlock = cond_block
        self.breakBlock = elihw_block

        if not self.block.block.is_terminated:
            self.block.branch(cond_block)
        self.block = ir.IRBuilder(cond_block)
        condition = self.visit(ctx.condition)
        if condition.type == i32:
            condition = self.block.icmp_signed("!=", condition, ir.Constant(i32, 0))
        self.block.cbranch(cond=condition, truebr=while_block, falsebr=elihw_block)

        self.block = ir.IRBuilder(while_block)
        self.visitCodeBlockNode(ctx.block)
        if not self.block.block.is_terminated:
            self.block.branch(cond_block)

        self.block = ir.IRBuilder(elihw_block)
        self.popSymbolTable()

        self.continueBlock = None
        self.breakBlock = None
        return

    def visitFunctionBody(self, ctx: FunctionBody):
        return self.default(ctx)

    def visitCodeBlockNode(self, ctx: CodeblockNode):
        self.pushSymbolTable(ctx.symbol_table)
        if self.current_function:
            for variable in self._symbol_table.variables.values():
                varnode: VariableNode = variable.node
                a: ir.AllocaInstr = self.block.alloca(varnode.getLLVMType(), 1, varnode.getName())
                variable.register = a
        else:
            for variable in self._symbol_table.variables.values():
                varnode: VariableNode = variable.node
                gv = ir.GlobalVariable(module=self.module, name=varnode.getName(), typ=varnode.getLLVMType())
                gv.linkage = "internal"
                variable.register = gv
                self.globals.append(gv)
        self.default(ctx)

        self.popSymbolTable()

    def visitTermNode(self, ctx: TermNode):
        return ctx.llvmValue()

    def visitUnOpNode(self, ctx: UnOpNode):
        pass

    def visitVariableNameNode(self, ctx: VariableNameNode):
        table_entry: VariableEntry = self._symbol_table.getTableEntry(ctx.getName(), not ctx.rvalue, True,
                                                                      metadata=ctx.getMetaData())
        ins: ir.Instruction = table_entry.register
        if ctx.rvalue:
            ins = self.block.load(ins, name=ctx.getName())
        return ins

    def visitVariableIntNode(self, ctx: VariableIntNode):
        return self.visitVariableNode(ctx)

    def visitVariableCharNode(self, ctx: VariableCharNode):
        return self.visitVariableNode(ctx)

    def visitVariableFloatNode(self, ctx: VariableFloatNode):
        return self.visitVariableNode(ctx)

    def visitVariableNode(self, ctx: VariableNode):
        return self.visitVariableNameNode(ctx)

    def visitFunctionNode(self, ctx: FunctionNode):
        functionnode = self._symbol_table.getFunction(ctx.functionName)
        fmt_args = self.visit(ctx.argumentNode)
        return self.block.call(functionnode.memorylocation, fmt_args)

    def visitScanfNode(self, ctx: ScanfNode):
        if not self.scanf:
            voidptr_ty = cchar.as_pointer()
            scanf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
            self.scanf = ir.Function(self.module, scanf_ty, name="scanf")
        fmt_args = self.visitArgumentNode(ctx.argumentNode)
        fmt_args = self.processStringArguments(fmt_args)
        return self.block.call(self.scanf, fmt_args)

    def gep(self, element):
        return self.block.gep(element, indices=[i32(0), i32(0)], inbounds=True, name=element.name)

    def processStringArguments(self, fmt_args):
        fmt_args[0] = self.gep(fmt_args[0])
        for index in range(1, len(fmt_args)):
            if hasattr(fmt_args[index].type, "pointee"):
                if isinstance(fmt_args[index].type.pointee, ir.ArrayType):
                    fmt_args[index] = self.gep(fmt_args[index])
                # else:
                #     fmt_args[index] = self.load(fmt_args[index])
        return fmt_args

    def visitPrintfNode(self, ctx: PrintfNode):
        if not self.printf:
            voidptr_ty = cchar.as_pointer()
            printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
            self.printf = ir.Function(self.module, printf_ty, name="printf")
        fmt_args = self.visitArgumentNode(ctx.argumentNode)
        fmt_args = self.processStringArguments(fmt_args)
        return self.block.call(self.printf, fmt_args)

    def visitArgumentNode(self, ctx: ArgumentsNode):
        arguments: list = []
        for arg in ctx.getChildren():
            arguments.append(self.visit(arg))
        return arguments

    def visitDerefNode(self, ctx: DeRefNode):
        ins = self.visit(ctx.child)
        ins = self.block.load(ins, name=ins.name)
        return ins

    def visitRefNode(self, ctx: RefNode):
        a: ir.Instruction = self._symbol_table.getTableEntry(ctx.child.getName()).register

        return a

    def visitReturnNode(self, ctx: ReturnNode):
        value = self.visit(ctx.child)
        if value:
            mem = self.current_function.return_address
            self.block.store(value, mem)
        ret_blo = self.current_function.return_block
        self.block.branch(ret_blo)
        # if value is None:
        #     self.block.ret_void()
        # else:
        #     self.block.ret(value)
        # return

    def visitIfElsestatementNode(self, ctx: IfElseStatementNode):
        self.pushSymbolTable(ctx.symbol_table)

        condition = self.visit(ctx.condition)
        if_block = self.block.function.append_basic_block(name='if')
        elseif_block = self.block.function.append_basic_block(name='elseif')
        endif_block = self.block.function.append_basic_block(name='endif')

        self.block.cbranch(cond=condition, truebr=if_block, falsebr=elseif_block)

        self.block = ir.IRBuilder(if_block)
        self.visitCodeBlockNode(ctx.block)
        if not self.block.block.is_terminated:
            self.block.branch(endif_block)

        self.block = ir.IRBuilder(elseif_block)
        self.visitCodeBlockNode(ctx.else_statement.block)
        if not self.block.block.is_terminated:
            self.block.branch(endif_block)

        self.block = ir.IRBuilder(endif_block)
        self.popSymbolTable()

    def visitIfstatementNode(self, ctx: IfstatementNode):
        self.pushSymbolTable(ctx.symbol_table)
        condition = self.visit(ctx.condition)
        if condition.type == i32:
            condition = self.block.icmp_signed("!=", condition, ir.Constant(i32, 0))

        if_block = self.block.function.append_basic_block(name='if')
        endif_block = self.block.function.append_basic_block(name='endif')

        self.block.cbranch(cond=condition, truebr=if_block, falsebr=endif_block)

        self.block = ir.IRBuilder(if_block)
        self.visitCodeBlockNode(ctx.block)
        if not self.block.block.is_terminated:
            self.block.branch(endif_block)

        self.block = ir.IRBuilder(endif_block)
        self.popSymbolTable()

        return

    def visitAssNode(self, ctx: AssNode):
        ctx.lhs.setRvalue(False)
        memoryloc = self.visit(ctx.lhs)
        if not self.current_function:
            gv = self.module.globals[ctx.lhs.getName()]
            gv.initializer = ctx.rhs.llvmValue()
            self._symbol_table.getTableEntry(ctx.lhs.getName()).register = gv
            return
        if isinstance(ctx.rhs, TermNode):
            a = ctx.rhs.llvmValue()
            return self.block.store(value=ctx.rhs.llvmValue(), ptr=memoryloc)
        value = self.visit(ctx.rhs)
        if value.type.is_pointer and not isinstance(ctx.rhs, RefNode):
            value = self.block.load(value, value.name)

        value = self.convertTo(value, ctx)
        return self.block.store(value, memoryloc)

    def visitPointerNode(self, ctx: PointerNode):
        if ctx.getChildren()[0] and isinstance(ctx._child, StringNode):
            return self.visit(ctx.getChildren()[0])
        # reg: ir.Instruction = self._symbol_table.getTableEntry(ctx.getName()).register

        return self.visitVariableNode(ctx)

    def visitArrayRefNode(self, ctx: ArrayRefNode):

        name = ctx.getName()
        index = ctx.index
        index = self.visit(index)
        entry: VariableEntry = self._symbol_table.getTableEntry(name)
        arr: ir.ArrayType = entry.register
        elem = self.block.gep(arr, indices=[i32(0), index], inbounds=True, name=name)
        if ctx.rvalue:
            elem = self.block.load(elem, name=ctx.getName())
        return elem

    def visitStringNode(self, ctx: StringNode):

        voidptr_ty = cchar.as_pointer()
        fmt = ctx.getFullString() + "\00"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=str(id(ctx)))
        # global_fmt.global_constant = True
        global_fmt.linkage = "internal"

        global_fmt.initializer = c_fmt
        self.globals.append(global_fmt)
        return global_fmt

    def visitBinOpNode(self, ctx: BinOpNode):
        v1: ir.Instruction = self.visit(ctx.lhs)
        v2 = self.visit(ctx.rhs)

        # copy and load to new reg
        if v1.type.is_pointer:
            v1 = self.block.load(v1, v1.name)
        if v2.type.is_pointer:
            v2 = self.block.load(v2)

        if ctx.getLLVMType() != v1.type:
            v1 = self.block.sitofp(v1, ctx.getLLVMType())
        if ctx.getLLVMType() != v2.type:
            v2 = self.block.sitofp(v2, ctx.getLLVMType())

        return v1, v2

    def visitBinPlusNode(self, ctx: BinPlusNode):
        v1, v2 = self.visitBinOpNode(ctx=ctx)

        # integer addition
        if ctx.type == TermIntNode or ctx.type == TermCharNode:
            return self.block.add(v1, v2)
        # fp addition
        return self.block.fadd(v1, v2)

    def visitBinLTENode(self, ctx: BinLTENode):
        return self.compOp(ctx, op='<=')

    def visitBinAndNode(self, ctx: BinAndNode):
        v1: ir.Instruction = self.visit(ctx.lhs)
        v2 = self.visit(ctx.rhs)
        # copy and load to new reg
        if v1.type.is_pointer:
            v1 = self.block.load(v1, v1.name)
        if v2.type.is_pointer:
            v2 = self.block.load(v2)
        if ctx.getLLVMType() != v1.type:
            v1 = self.block.icmp_signed("!=", v1, ir.Constant(i32, 0))
        if v2.type:
            v2 = self.block.icmp_signed("!=", v2, ir.Constant(i32, 0))
        return self.block.and_(v1, v2)

    def visitBinOrNode(self, ctx: BinOrNode):
        super().visitBinOrNode(ctx)

    def visitBinEQNode(self, ctx: BinEQNode):
        return self.compOp(ctx, op='==')

    def visitBinModNode(self, ctx: BinModNode):
        lhs = self.load(self.visit(ctx.lhs))
        rhs = self.load(self.visit(ctx.rhs))
        return self.block.srem(lhs,rhs)

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

    def load(self, ins: ir.AllocaInstr):
        if not isinstance(ins, ir.AllocaInstr) and not isinstance(ins, ir.GlobalVariable) and not isinstance(ins, ir.GEPInstr):
            return ins
        else:
            name = ins.name
            ins = self.block.load(ins, name=name)
            return ins

    def compOp(self, ctx: BinOpNode, op):
        lhs = self.load(self.visit(ctx.lhs))
        rhs = self.load(self.visit(ctx.rhs))
        return self.block.icmp_signed(cmpop=op, lhs=lhs, rhs=rhs)

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
            ctxtype = ctx.getLLVMType()
            if ctxtype == cfloat and value.type == i32:
                return self.block.sitofp(value, ctx.getLLVMType())
            if ctxtype == i32 and value.type == cfloat:
                return self.block.fptosi(value, ctx.getLLVMType())
        return value
