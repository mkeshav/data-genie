start: instruction+

instruction: "apply checks" code_block -> predicates

checks: has_size
        | has_columns
        | is_unique
        | not_null
        | is_positive
        | is_in
        | quantile
        | is_date

code_block: "{" checks+ "}"

has_size: "size is " SIGNED_NUMBER
has_columns: "has columns" array
is_unique: "column" NAME "has unique values"
not_null: "column" NAME "is not null"
is_positive: "column" NAME "has positive values"
is_in: "column" NAME "in" array
quantile: "column" NAME "quantile(" QUANTILE ")" COMPARATOR SIGNED_NUMBER
is_date: "column" NAME "is date"

array  : "[" [ESCAPED_STRING ("," ESCAPED_STRING)*] "]"

QUOTED_STRING: "'" NAME "'"
QUANTILE: "0." _INT
LT: "<"
GT: ">"
EQ: "=="
COMPARATOR: (LT | GT | EQ )

WHITESPACE: (" " | "\\n")+
%ignore WHITESPACE

%import common.LETTER
%import common.SIGNED_NUMBER
%import common.NUMBER
%import common.WS
%import common.ESCAPED_STRING
%import common.CNAME -> NAME
%import common.FLOAT -> FLOAT
%import common.INT -> _INT

%ignore WS