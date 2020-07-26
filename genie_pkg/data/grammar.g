start: instruction+

instruction: "apply checks" code_block -> predicates

checks: has_size
        | has_columns
        | is_unique
        | not_null
        | is_positive
        | is_in

code_block: "{" checks+ "}"

has_size: "size is " SIGNED_NUMBER
has_columns: "has columns" array
is_unique: "column" COLUMN_NAME "has unique values"
not_null: "column" COLUMN_NAME "is not null"
is_positive: "column" COLUMN_NAME "has positive values"
is_in: "column" COLUMN_NAME "in" array

array  : "[" [QUOTED_STRING ("," QUOTED_STRING)*] "]"

COLUMN_NAME: LETTER+
QUOTED_STRING: "'" LETTER+ "'"

WHITESPACE: (" " | "\\n")+
%ignore WHITESPACE

%import common.LETTER
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS