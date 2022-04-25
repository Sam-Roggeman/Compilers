
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
If the comparison fails, an errormessage will be displayed. 





#Features
A: Present in AST
L: Runnable LLVM Code-Generation
M: Runnable Mips Code-Generation
X: Not working or not implemented


|     | Functionality                                   | Status |
|-----|-------------------------------------------------|--------|
| 1   | Binary operations +, -, *, and /.               | L      |
|     | Binary operations >, <, and ==.                 | L      |
|     | + and -                                         | L      |
|     | Brackets to overwrite the order of operations.  | L      |
|     | Logical operators &&, or, and !.                | L      |
|     | Comparison operators >=, <=, and !=.            | L      |
|     | Binary operator %.                              | L      |
|     | Visualization in the form of dot using graphviz | L      |
|     | Constant Folding                                | L      |
| 2   | Types                                           | L      |
|     | Reserved words                                  | L      |
|     | Variables                                       | L      |
|     | Pointer operations                              | L      |
|     | Identifier operations                           | L      |
|     | Conversions                                     | L      |
| 3   | Comments                                        | A      |
|     | Printf                                          | L      |
|     | Written Comment -> LLVM                         | X      |
|     | Extra comments -> LLVM                          | X      |
| 4   | Reserved words                                  | A      |
|     | for                                             | A      |
|     | break                                           | A      |
|     | continue                                        | A      |
|     | scopes                                          | A      |
|     | switch, case and default                        | A      |
| 5   | Reserved words                                  | A      |
|     | Scopes                                          | A      |
|     | Local and global variables                      | A      |
|     | functions                                       | A      |
|     | Unreachable and dead code                       | A      |
|     | not generating code after break and continue    | A      |
| 6   | Arrays                                          | A      |
|     | Multi-dimensional arrays                        | X      |
|     | dynamic arrays                                  | X      |
|     | Import                                          | A      |