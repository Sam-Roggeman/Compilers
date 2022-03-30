grammar CGrammar2;

startRule
    :(expr SEMICOL)* EOF
    ;


expr
    : mathExpr
    | declaration
    | assignment
    | declaration_assignment
    | reference
    | variable
    ;

rvalue: mathExpr| variable ;
function: printf;
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
    // (||,&&)
    | mathExpr logOp mathExpr
    // (<,>,==,<=,>=,!=)
    | mathExpr compOp mathExpr
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
AND: '&&';
OR: '||';
NOT: '!';
LTE: '<=';
GTE: '>=';
NE: '!=';
MOD: '%';

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