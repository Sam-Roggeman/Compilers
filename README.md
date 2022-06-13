
#How to run
We made three scripts:

The first one is the build script which takes no arguments and makes the virtual environment 
and downloads the needed packages. It also processes the grammar/

The second one is the run script which takes one argument which is “./inputfiles/” ${path/to/cfile.c} where cfile.c if the file that should be compiled.
The ./output folder will contain the dot-output for the ast. For example ./run.sh Test.c


The last script takes no input parameters and will compile all of the c files from the project folders in inputfiles.
It will save all of the output (also terminal output) to ./testfiles/{project}/testOutput and compare it with
./testfiles/{project}/expectedOutput, the result is found in ./testfiles/{project}/Result.txt 
where True means that the files are the same. There will also be terminal output saying if the test has passed or not. 
If the comparison fails, an errormessage will be displayed. <br>
WARNING: THESE WILL PROBABLY ALL FAIL AT THE MOMENT AS A LOT OF THE CORE HAS BEEN CHANGED AND THE TESTS NOT UPDATED




#Features
A: Present in AST
L: Runnable LLVM Code-Generation
M: Runnable Mips Code-Generation
X: Not working or not implemented
If you see the symbol N after either M or L it means that the llvm part of these features were fixed since the last deadline

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