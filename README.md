<h3>#How to run </h3>
<h3>Scripts</h3>
<h6>Build: </h6>
No arguments, creates the virtual environment and installs the needed packages and compiles the grammar.
<h6>Run:</h6>
**Arguments:** $1: filepath <br>
**Flags:** -M (compile to MIPS), -L (Compile to LLVM), -R (Run LLVM code using LLVM backend),
-D (Make dot diagram before and after optimalizations). <br>
**Use:** Compiles a single c file. The output will be saved to ./output.

<h6>RunAll:</h6>
**Flags:** -M (compile to MIPS), -L (Compile to LLVM), -R (Run LLVM code using LLVM backend),
-D (Make dot diagram before and after optimalizations). <br>
**Use:** Compiles all c files from ./inputFiles/CompilersBenchmark. The output will be saved to ./output.

<h6>TestScript:</h6>
**Use:** Compiles all c files from ./inputFiles/CompilersBenchmark. Will run LLVM code and compare it to the expected
output of the c program. Will save all the output of the code to testOutput in ./testFiles. Any file compare errors will be logged in
comparisonErrors.txt and test-results are found in Result.txt.

<h3>#Features</h3>
**A:** Present in AST <br>
**L:** Runnable LLVM Code-Generation <br>
**M:** Runnable Mips Code-Generation <br>
**X:** Not working or not implemented <br>
**N:** LLVM part of these features were added since the first deadline

|     | Functionality                                   | Status                                  |
|-----|-------------------------------------------------|-----------------------------------------|
| 1   | Binary operations +, -, *, and /.               | M                                       |
|     | Binary operations >, <, and ==.                 | M                                       |
|     | Unary operators + and -                         | M (this doesn't work for arrays)        |
|     | Brackets to overwrite the order of operations.  | M                                       |
|     | Logical operators &&, or, and !.                | M                                       |
|     | Comparison operators >=, <=, and !=. (opt)      | M                                       |
|     | Binary operator %. (opt)                        | M                                       |
|     | Visualization in the form of dot using graphviz | M                                       |
|     | Constant Folding                                | M                                       |
| 2   | Types                                           | M                                       |
|     | Reserved words                                  | M                                       |
|     | Variables                                       | M                                       |
|     | Pointer operations                              | L                                       |
|     | Identifier operations (opt)                     | M (this doesn't work for arrays)        |
|     | Conversions (opt)                               | M                                       |
| 3   | Comments                                        | A                                       |
|     | Printf                                          | M (this doesn't work for arrays)        |
|     | Written Comment -> LLVM (opt)                   | X                                       |
|     | Extra comments -> LLVM (opt)                    | X                                       |
| 4   | Reserved words                                  | M  N                                    |
|     | for                                             | M  N                                    |
|     | break                                           | M  N                                    |
|     | continue                                        | M  N                                    |
|     | scopes                                          | L  N                                    |
|     | switch, case and default (opt)                  | X                                       |
| 5   | Reserved words                                  | M  N                                    |
|     | Scopes                                          | L  N                                    |
|     | Local and global variables                      | M  N                                    |
|     | functions                                       | M  N                                    |
|     | Unreachable and dead code                       | M  N                                    |
|     | not generating code after break and continue    | M  N                                    |
| 6   | Arrays                                          | L  N                                    |
|     | Multi-dimensional arrays (opt)                  | X                                       |
|     | dynamic arrays (opt)                            | X                                       |
|     | Import                                          | M  N (only printf, scanf works in llvm) |

<h3>#All testfiles and their status </h3>
[Trello-Screenshot](https://prnt.sc/sjEybNBmtcvT)
