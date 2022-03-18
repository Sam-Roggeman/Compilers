grammar CGrammar;
startRule
    :expr* EOF
    ;


expr
    : mathExpr
    | type variable
    | variable ASS expr
    | (CONST)? type variable ASS expr
    | REF variable
    | variable
    | expr SEMICOL
    ;

variable
    : MUL variable
    | VarName
    ;



mathExpr
    : (PLUS|MIN|NOT) mathExpr
    | mathExpr (MUL|DIS|MOD) mathExpr
    | mathExpr (PLUS | MIN) mathExpr
    | mathExpr (AND|OR) mathExpr
    | mathExpr (LT|GT|EQ|LTE|GTE|NE) mathExpr
    | LBR mathExpr RBR
    | value
    | variable
    ;
binOp: PLUS | MIN  |DIS| MUL |MOD;
unOp: PLUS|MIN;
logOp: AND|OR;
compOp: LT|GT|EQ|LTE|GTE|NE;
type: CHARTYPE|FLOATTYPE|INTTYPE| type MUL;
value: INT|FLOAT|CHAR;

INT:'0' | [1-9] [0-9]*;
FLOAT: [0-9]+[.][0-9]+[f];
CHAR: ['].['];

CONST: 'const';
MUL:'*';
MIN:'-';
DIS:'/';
PLUS:'+';
LT:'<';
GT:'>';
EQ:'==';
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
SEMICOL: ';';
CHARTYPE: 'char';
FLOATTYPE: 'float';
INTTYPE: 'int';
VarName: [A-Za-z_] [A-Za-z_0-9]*;
REF: '&';

BlockComment: '/*' .*? '*/' -> skip;
Comment: '//' ~[\n]* -> skip;
WS: [ \n\t\r]+ -> skip;