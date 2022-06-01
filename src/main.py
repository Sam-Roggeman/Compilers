import sys
from antlr4 import *

from g4_files.CGrammarLexer import CGrammarLexer
from g4_files.CGrammarParser import CGrammarParser
from CSTVisitor import CGrammarVisitorImplementation
from AST import *
from ASTVisitor import *

def main(argv):
    name = argv[1]
    inputlocation = name
    if "./inputFiles/" not in name:
        inputlocation = "./inputFiles/" + name
    else:
        name = name[13:-2]

    input_stream = FileStream(inputlocation)
    lexer = CGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CGrammarParser(stream)
    tree = parser.startRule()
    visitor = CGrammarVisitorImplementation()
    a = AST(root=visitor.visitStartRule(ctx=tree), name=name)

    a.exportToLLVM(run=True)


def printfTest():
    m = ir.Module()
    func_ty = ir.FunctionType(ir.VoidType(), [])
    i32_ty = ir.IntType(32)
    func = ir.Function(m, func_ty, name="printer")

    voidptr_ty = ir.IntType(8).as_pointer()

    fmt = "%i; "
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                        bytearray(fmt.encode("utf8")))
    global_fmt = ir.GlobalVariable(m, c_fmt.type, name="str")
    global_fmt.global_constant = True
    global_fmt.initializer = c_fmt

    printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
    printf = ir.Function(m, printf_ty, name="printf")

    builder = ir.IRBuilder(func.append_basic_block('entry'))

    # this val can come from anywhere
    int_val = builder.add(i32_ty(5), i32_ty(3))

    fmt_arg = builder.bitcast(global_fmt, voidptr_ty)
    builder.call(printf, [fmt_arg, int_val])
    print(str(m))

    builder.ret_void()




if __name__ == '__main__':
    main(sys.argv)
    # printfTest()
