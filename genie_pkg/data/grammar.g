start: instruction+

instruction: "apply checks" code_block -> predicates

checks: row_count
        | has_columns
        | is_unique
        | not_null
        | is_positive
        | has_one_of
        | quantile
        | is_date
        | value_length
        | percent_value_length

code_block: "{" checks+ "}"

row_count: "row_count" COMPARATOR SIGNED_NUMBER
has_columns: "has_columns(" array ")"
is_unique: "is_unique(" NAME ")"
not_null: "is_not_null(" NAME ")"
is_positive: "is_positive(" NAME ")"
has_one_of: "has_one_of(" NAME "," array ")"
quantile: "quantile(" NAME "," QUANTILE ")" COMPARATOR SIGNED_NUMBER
is_date: "is_date(" NAME ")"
value_length: "value_length(" NAME ","? "ignore_nulls="? BOOL? ")" EQ SIGNED_NUMBER
percent_value_length: "percent_of_values_have_length(" NAME  "," "pass_percent_threshold=" SIGNED_NUMBER ","? "ignore_nulls="? BOOL? ")" EQ SIGNED_NUMBER

array  : "[" [ESCAPED_STRING ("," ESCAPED_STRING)*] "]"

QUANTILE: "0." _INT
LT: "<"
GT: ">"
EQ: "=="
COMPARATOR: (LT | GT | EQ )
BOOL: ("False" | "True")

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