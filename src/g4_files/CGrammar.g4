grammar CGrammar;

startRule
    : file EOF
    ;

file
    : (include)* ((expr SEMICOL) | (statement) | (function))*
    ;

body
    : ((functioncall SEMICOL)
    |  (statement)  | (expr SEMICOL)
    | (printf SEMICOL))*  (BREAK SEMICOL (expr)*
    | CONTINUE SEMICOL (expr SEMICOL)*)?
    | RETURN expr SEMICOL
    ;

expr
    : mathExpr
    | declaration
    | assignment
    | declaration_assignment
    | reference
    | variable (array)?
    | string
    ;

statement
    : ifstatement
    | ifelsestatement
    | whilestatement
    | forstatement
    ;

ifelsestatement: ifstatement elsestatement;

rvalue: mathExpr| variable (array)? ;

include: INCLUDE library;
library: '<' 'stdio' '.' 'h' '>';

function: printf SEMICOL | functiondeclaration SEMICOL| functiondefinition | functioncall SEMICOL;
functiondeclaration: (types_specifier | VOID) VarName LBR (arguments?) RBR;
functiondefinition: (types_specifier | VOID) VarName LBR (arguments?) RBR LCBR functionbody RCBR;
functionbody: ((expr SEMICOL) | (statement) | (functioncall SEMICOL) | (printf SEMICOL))* (RETURN (expr | literal)? SEMICOL (expr SEMICOL)*)?;
functioncall: VarName LBR (arguments)? RBR;


array: (LSBR INTLit RSBR)+;
ifstatement: IF LBR expr  RBR LCBR (body) RCBR;
elsestatement: ELSE LCBR (body) RCBR;
whilestatement: WHILE LBR expr RBR LCBR (body) RCBR;
forstatement: FOR LBR initializer SEMICOL condition SEMICOL incrementer RBR LCBR (body) RCBR;
condition: expr;
initializer: expr;
incrementer: expr;

declaration: (CONST)? types_specifier variable (array)?(COMMA)? declarationloop? ;
declarationloop: (variable COMMA?| variable ASS rvalue COMMA? | variable ASS functioncall COMMA? | variable ASS (REF)* variable COMMA?)*;
declaration_assignment
    : (CONST)? types_specifier variable (array)? ASS rvalue
    |(CONST)? types_specifier variable (array)? ASS functioncall
    | (CONST)? pointertype variable (array)? ASS (REF)* variable
    | (CONST)? pointertype variable
    ;
assignment
    : (variable (array)?|dereffedvariable) ASS rvalue
    | (variable (array)?|dereffedvariable) ASS (REF)* variable
    ;
reference: REF variable;

binOp: binOpPrio2
    | compOp
    | logOp
    | binOpPrio1
    ;

mathExpr : unOp mathExpr
    | mathExpr incr_decr
    // (/,*,%)
    | mathExpr binOpPrio2 mathExpr
    // (+,-)
    | mathExpr binOpPrio1 mathExpr
    // (<,>,==,<=,>=,!=)
    | mathExpr compOp mathExpr
        // (||,&&)
    | mathExpr logOp mathExpr

    | incr_decr mathExpr
    // ((,))
    | LBR mathExpr RBR

    | functioncall binOpPrio1 functioncall
    | functioncall binOpPrio2 functioncall
    | functioncall compOp functioncall
    | functioncall logOp functioncall
    | literal
    | variable (array)?
    | dereffedvariable
    ;
incr_decr: incr|decr;
decr: MIN MIN;
incr: PLUS PLUS;
pointer: MUL;
pointertype: (CONST)? types_specifier pointer | pointertype pointer;
dereffedvariable:  deref variable;
binOpPrio2: DIS| mul |MOD;
binOpPrio1: PLUS | MIN;
compOp: LT|GT|EQ|LTE|GTE|NE;
unOp: PLUS|MIN|NOT;
logOp: AND|OR;
mul: MUL;
deref: MUL (MUL)*;
variable: VarName;


types_specifier: CHARTYPE|FLOATTYPE|INTTYPE;
literal: INTLit|FLOATLit|CHARLit;
const_qualifier: CONST;

printf: 'printf' LBR (arguments?) RBR;
arguments: arg (COMMA arg)*;
arg: ( string | expr | (deref)* variable (array)? | literal | mathExpr | functioncall);
string: STRING;
//types_specifiers
CHARTYPE: 'char';
FLOATTYPE: 'float';
INTTYPE: 'int';

//literal
INTLit: '0' | [1-9] [0-9]*;
FLOATLit: [0-9]+[.][0-9]+[f]?;
CHARLit: [']SingleChar['];

//const_qualifier
CONST: 'const';

//binops
COMMA:',';
EQ:'==';
MUL:'*';
MIN:'-';
PLUS:'+';
DIS:'/';
LT:'<';
GT:'>';
ASS:'=';
LBR: '(';
RBR: ')';
LCBR: '{';
RCBR: '}';
LSBR: '[';
RSBR: ']';
AND: '&&';
OR: '||';
NOT: '!';
LTE: '<=';
GTE: '>=';
NE: '!=';
MOD: '%';
IF: 'if';
ELSE: 'else';
WHILE: 'while';
FOR: 'for';
BREAK: 'break';
CONTINUE: 'continue';
VOID: 'void';
//semicolon
SEMICOL: ';';
STRING: '"' SingleChar* '"';



REF: '&';
RETURN: 'return';
VarName: [A-Za-z_] [A-Za-z_0-9]*;

LINE_COMMENT
  : '//' ~[\r\n]* (EOF|'\r'? '\n') -> channel(HIDDEN)
  ;
BlockComment: '/*' .*? '*/' -> skip;
Comment: '//' ~[\n]* -> skip;
WS: [ \n\t\r]+ -> skip;

INCLUDE: '#include';
fragment ESC      : '\\' . ;
fragment SingleChar : ~('"'| '\\') | ESC ;