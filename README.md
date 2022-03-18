
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
V: Working   
X: Not working or not implemented


|    | Functionality                                   | Status |
|----|-------------------------------------------------|--------|
| 1  | Binary operations +, -, *, and /.               | V      |
|    | Binary operations >, <, and ==.                 | V      |
|    | + and -                                         | V      |
|    | Brackets to overwrite the order of operations.  | V      |
|    | Logical operators &&, or, and !.                | V      |
|    | Comparison operators >=, <=, and !=.            | V      |
|    | Binary operator %.                              | V      |
|    | Visualization in the form of dot using graphviz | V      |
|    | Constant Folding                                | V      |
| 2  | Types                                           | V      |
|    | Reserved words                                  | V      |
|    | Variables                                       | V      |
|    | Pointer operations                              | V      |
|    | Identifier operations                           | X      |
|    | Conversions                                     | V      |
| 3  | Comments                                        | V      |
|    | Printf                                          | V      |
|    | LLVM                                            | X      |
|    | Written Comment -> LLVM                         | X      |
|    | Extra comments -> LLVM                          | X      |
