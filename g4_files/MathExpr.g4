grammar MathExpr;

expr
    : expr SUM expr

    | INT
    ;

INT:'0' | [1-9] [0-9]*;
MUL:[\\*];
SUM:[+];
WS: [ \n\t\r]+ -> skip;