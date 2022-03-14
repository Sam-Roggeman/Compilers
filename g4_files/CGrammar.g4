grammar CGrammar;
startRule
    :expr* EOF
    ;
expr
    : type VarName
    | VarName ASS
    | type VarName ASS value
    | expr SEMICOL
    | mathExpr
    ;
mathExpr
    : mathExpr (MUL|DIS|MOD) mathExpr
    | mathExpr (PLUS | MIN) mathExpr
    | (PLUS|MIN|NOT) mathExpr
    | mathExpr (AND|OR) mathExpr
    | mathExpr (LT|GT|EQ|LTE|GTE|NE) mathExpr
    | LBR mathExpr RBR
    | value
    ;
binOp: PLUS | MIN  |DIS| MUL |MOD;
unOp: PLUS|MIN;
logOp: AND|OR;
compOp: LT|GT|EQ|LTE|GTE|NE;
type: CHARTYPE|FLOATTYPE|INTTYPE| type MUL;
value: INT|FLOAT|CHAR;

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
CHARTYPE: 'char';
FLOATTYPE: 'float';
INTTYPE: 'int';
VarName: [A-Za-z_] [A-Za-z_0-9]*;

WS: [ \n\t\r]+ -> skip;