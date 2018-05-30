%{
#include <stdio.h>
%}

%token ASSIGN CASE CASEARROW CLASS ESAC ELSE FALSE FI ID IF IN INHERITS INTEGER ISVOID LET LESSEQUAL LOOP NEW NOT OF POOL STRING THEN TRUE TYPE WHILE

%%

program: class ';'
       | program class ';'
       ;

class: CLASS TYPE inherits '{' features '}'
     ;

inherits: %empty
        | INHERITS TYPE
        ;

features: %empty
        | feature ';'
        | features feature ';'
        ;

feature: ID '(' formals ')' ':' TYPE '{' expr '}'
       | binding
       ;

binding: ID ':' TYPE initializer
       ;

formals: formal
       | formals formal
       ;

formal: ID ':' TYPE
      ;

initializer: %empty
           | ASSIGN expr
           ;

expr: ID ASSIGN expr
    | expr baseclass '.' ID '(' invokeparams ')'
    | ID '(' invokeparams ')'
    | IF expr THEN expr ELSE expr FI
    | WHILE expr LOOP expr POOL
    | '{' exprs '}'
    | LET letbindings IN expr
    | CASE expr OF casebody ESAC
    | NEW TYPE
    | ISVOID expr
    | expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    | '~' expr
    | expr '<' expr
    | expr LESSEQUAL expr
    | expr '=' expr
    | NOT expr
    | '(' expr ')'
    | ID
    | INTEGER
    | STRING
    | TRUE
    | FALSE
    ;

casebody: case
        | casebody case
        ;

case: ID ':' TYPE CASEARROW expr ';'
    ;

letbindings: binding
           | letbindings ',' binding
           ;

exprs: expr ';'
     | exprs expr ';'
     ;

invokeparams: %empty
            | expr
            | invokeparams ',' expr
            ;

%%
