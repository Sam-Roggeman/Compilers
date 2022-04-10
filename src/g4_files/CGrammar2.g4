grammar CGrammar2;

startRule
    : file EOF
    ;

file
    : ((expr SEMICOL) | (statement))*
    ;

expr
    : mathExpr
    | declaration
    | assignment
    | declaration_assignment
    | reference
    | variable
    | BREAK
    | CONTINUE
    ;

statement
    : ifstatement (elsestatement)?
    | whilestatement
    | forstatement
    ;

rvalue: mathExpr| variable ;
function: printf;

ifstatement: IF LBR expr  RBR LCBR file RCBR;
elsestatement: ELSE LCBR file RCBR;
whilestatement: WHILE LBR expr RBR LCBR file RCBR;
forstatement: FOR LBR expr SEMICOL expr SEMICOL expr RBR LCBR file RCBR;

declaration: (CONST)? types_specifier variable;
declaration_assignment
    : (CONST)? types_specifier variable ASS rvalue
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
deref: MUL;
variable: VarName;


types_specifier: CHARTYPE|FLOATTYPE|INTTYPE;
literal: INTLit|FLOATLit|CHARLit;
const_qualifier: CONST;
printf: 'printf' '(' (variable | literal) ')';


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

//semicolon
SEMICOL: ';';

REF: '&';

VarName: [A-Za-z_] [A-Za-z_0-9]*;

LINE_COMMENT
  : '//' ~[\r\n]* (EOF|'\r'? '\n') -> channel(HIDDEN)
  ;
BlockComment: '/*' .*? '*/' -> skip;
Comment: '//' ~[\n]* -> skip;
WS: [ \n\t\r]+ -> skip;