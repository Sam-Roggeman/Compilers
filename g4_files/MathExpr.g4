grammar MathExpr;
startRule
    :expr SEMICOL
    ;
expr
    : expr binOp expr
    | unOp expr
    | LBR expr RBR
    | INT
    ;
binOp: PLUS | MIN | DIS | MUL|MOD;
unOp: PLUS|MIN;
logOp: AND|NOT|OR;
compOp: LT|GT|EQ|LTE|GTE|NE;

INT:'0' | [1-9] [0-9]*;
MUL:'*';
PLUS:'+';
MIN:'-';
DIS:'/';
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