grammar CGrammar;

startRule
    : file EOF
    ;

file
    : (include)* ((expr SEMICOL) | (statement) | (function))*
    ;

body
    : ((functioncall SEMICOL) |(expr SEMICOL) | (statement)  | (printf SEMICOL))*  (BREAK SEMICOL | CONTINUE SEMICOL)?;

expr
    : mathExpr
    | declaration
    | assignment
    | declaration_assignment
    | reference
    | variable
    | string
    ;

statement
    : ifstatement (elsestatement)?
    | whilestatement
    | forstatement
    ;

rvalue: mathExpr| variable ;

include: INCLUDE library;
library: '<' VarName '.' 'h' '>';

function: printf SEMICOL | functiondefinition | functioncall SEMICOL;
functiondefinition: (types_specifier | VOID) VarName LBR (arguments?) RBR LCBR functionbody RCBR;
functionbody: ((expr SEMICOL) | (statement) | (functioncall SEMICOL) | (printf SEMICOL))* (RETURN (expr | literal) SEMICOL)?;
functioncall: VarName LBR (arguments)? RBR;


array: (LSBR expr RSBR)+;
ifstatement: IF LBR expr  RBR LCBR (body) RCBR;
elsestatement: ELSE LCBR (body) RCBR;
whilestatement: WHILE LBR expr RBR LCBR (body) RCBR;
forstatement: FOR LBR expr SEMICOL expr SEMICOL expr RBR LCBR (body) RCBR;


declaration: (CONST)? types_specifier variable;
declaration_assignment
    : (CONST)? types_specifier variable ASS rvalue
    |(CONST)? types_specifier variable ASS functioncall
    | (CONST)? pointertype variable ASS (REF)* variable
    ;
assignment
    : (variable|dereffedvariable) ASS rvalue
    | (variable|dereffedvariable) ASS (REF)* variable
    ;
reference: REF variable;

binOp: binOpPrio2
    | compOp
    | logOp
    | binOpPrio1
    ;

mathExpr : unOp mathExpr
    // (/,*,%)
    | mathExpr binOpPrio2 mathExpr
    // (+,-)
    | mathExpr binOpPrio1 mathExpr
    // (<,>,==,<=,>=,!=)
    | mathExpr compOp mathExpr
        // (||,&&)
    | mathExpr logOp mathExpr
    // ((,))
    | LBR mathExpr RBR
    | literal
    | variable
    ;
pointer: MUL;
pointertype: (CONST)? types_specifier pointer | pointertype pointer;
dereffedvariable: deref variable;
binOpPrio2: DIS| mul |MOD;
binOpPrio1: PLUS | MIN;
compOp: LT|GT|EQ|LTE|GTE|NE;
unOp: PLUS|MIN|NOT;
logOp: AND|OR;
mul: MUL;
deref: MUL (MUL)*;
variable: VarName|array;


types_specifier: CHARTYPE|FLOATTYPE|INTTYPE;
literal: INTLit|FLOATLit|CHARLit;
const_qualifier: CONST;

printf: 'printf' LBR (arguments?) RBR;
arguments: arg (COMMA arg)*;
arg: ( string | (deref)* variable | literal | mathExpr);
string: STRING;
//types_specifiers
CHARTYPE: 'char';
FLOATTYPE: 'float';
INTTYPE: 'int';

//literal
INTLit: '0' | [1-9] [0-9]*;
FLOATLit: [0-9]+[.][0-9]+[f];
CHARLit: ['].['];

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
STRING: '"' ~('"')* '"';



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