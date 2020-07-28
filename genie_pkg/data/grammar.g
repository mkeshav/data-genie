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
has_columns: "has_columns(" array ")"
is_unique: "is_unique(" NAME ")"
not_null: "is_not_null(" NAME ")"
is_positive: "is_positive(" NAME ")"
is_in: "has_one_of(" NAME "," array ")"
quantile: "quantile(" NAME "," QUANTILE ")" COMPARATOR SIGNED_NUMBER
is_date: "is_date(" NAME ")"

array  : "[" [ESCAPED_STRING ("," ESCAPED_STRING)*] "]"

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