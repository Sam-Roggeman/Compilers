from llvmlite import ir

# Create some useful types
cfloat = ir.DoubleType()
i32 = ir.IntType(32)
cchar = ir.IntType(8)
cbool = ir.IntType(1)
pointer =ir.PointerType