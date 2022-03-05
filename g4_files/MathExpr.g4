grammar MathExpr;
startRule
    :expr* EOF
    ;
expr
    : expr (MUL|DIS|MOD) expr
    | expr (PLUS | MIN) expr
    | (PLUS|MIN|NOT) expr
    | expr (AND|OR) expr
    | expr (LT|GT|EQ|LTE|GTE|NE) expr
    | LBR expr RBR
    | expr SEMICOL
    | INT
    ;
binOp: PLUS | MIN  |DIS| MUL |MOD;
unOp: PLUS|MIN;
logOp: AND|OR;
compOp: LT|GT|EQ|LTE|GTE|NE;

INT:'0' | [1-9] [0-9]*;
MUL:'*';
MIN:'-';
DIS:'/';
PLUS:'+';
LT:'<';
GT:'>';
EQ:'==';
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

WS: [ \n\t\r]+ -> skip;