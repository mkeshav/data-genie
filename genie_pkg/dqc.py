import pandas as pd
import pandas_flavor as pf
from lark import Lark, Tree
from pkg_resources import resource_string
from typing import Tuple, List
from genie_pkg import GenieException
import numpy as np


@pf.register_dataframe_accessor('dqc')
class QualityChecker(object):
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj
        self.ignore_column_case = False

    @staticmethod
    def _validate(obj):
        if obj.dropna(axis='columns', how='all').empty:
            raise AttributeError("DataFrame is empty!!! What quality do you expect from emptiness")

    @staticmethod
    def _comparator_to_fn(comparator: str, rhs):
        if comparator == ">":
            return lambda lhs: lhs > rhs
        if comparator == "==":
            return lambda lhs: lhs == rhs
        if comparator == "<":
            return lambda lhs: lhs < rhs
        else:
            return lambda _: False

    def _treat_column_name(self, column_name: str) -> str:
        if self.ignore_column_case:
            return column_name.lower()
        return column_name

    def _apply_quantile(self, node) -> Tuple[str, bool]:
        column_name = self._treat_column_name(node.children[0])
        q = float(node.children[1])
        c = node.children[2]
        rhs = float(node.children[3])
        lhs = self._obj[column_name].quantile(q)
        return node.data, self._comparator_to_fn(c, rhs)(lhs)

    def _apply_date_validation(self, node) -> Tuple[str, bool]:
        column_name = self._treat_column_name(node.children[0])
        try:
            pd.to_datetime(self._obj[column_name])
            return node.data, True
        except Exception as _:
            return "Date parse error: {0} for {1}".format(node.data, node.children[0]), False

    def _apply_has_one_of(self, node) -> Tuple[str, bool]:
        column_name = self._treat_column_name(node.children[0])
        allowed_values = [ct.value.replace("\"", "") for ct in node.children[1].children]
        unique_values = self._obj[column_name].unique()

        if len(node.children) == 2:
            ignore_case = False
        else:
            if node.children[2] == 'True':
                ignore_case = True
            else:
                ignore_case = False
        if ignore_case:
            allowed_values = [v.lower() for v in allowed_values]
            unique_values = [v.lower() for v in unique_values]

        return node.data, all(elem in allowed_values for elem in unique_values)

    def _apply_value_length(self, node) -> Tuple[str, bool]:
        column_name = self._treat_column_name(node.children[0])
        if len(node.children) == 3:
            ignore_nulls = 'False'
            comparator = node.children[1]
            rhs = int(node.children[2])
        else:
            ignore_nulls = node.children[1]
            comparator = node.children[2]
            rhs = int(node.children[3])

        if ignore_nulls == 'False':
            unique_lengths = self._obj[column_name].astype(str).map(len).unique()
        else:
            not_na_df = self._obj.replace(r'^\s*$', np.NaN, regex=True)[column_name].dropna().reset_index()
            unique_lengths = not_na_df[column_name].astype(str).map(len).unique()
        compare_fn = self._comparator_to_fn(comparator, rhs)
        return node.data, len(unique_lengths) == 1 and compare_fn(unique_lengths[0])

    def _apply_percent_value_length(self, node) -> Tuple[str, bool]:
        column_name = self._treat_column_name(node.children[0])
        if len(node.children) == 4:
            ignore_nulls = 'False'
            percent = int(node.children[1])
            rhs = int(node.children[3])
        else:
            percent = int(node.children[1])
            ignore_nulls = node.children[2]
            rhs = int(node.children[4])

        self._obj['length'] = self._obj[column_name].fillna('').astype(str).map(len)
        if ignore_nulls == 'True':
            not_na_df = self._obj.replace(r'^\s*$', np.NaN, regex=True).dropna()
        else:
            not_na_df = self._obj

        passing = not_na_df[not_na_df['length'] == rhs]
        return node.data, (passing.shape[0]/self._obj.shape[0])*100 >= percent

    def _apply_has_columns(self, node) -> Tuple[str, bool]:
        column_names = [ct.value.replace("\"", "") for ct in node.children[0].children]
        if len(node.children) == 1:
            ignore_case = False
        else:
            if node.children[1] == 'True':
                ignore_case = True
            else:
                ignore_case = False

        if ignore_case:
            expected_columns = [c.lower() for c in column_names]
            columns_in_df = list(map(str.lower, self._obj.columns))
        else:
            expected_columns = column_names
            columns_in_df = self._obj.columns

        return node.data, len(set(columns_in_df).intersection(expected_columns)) == len(set(expected_columns))

    @staticmethod
    def _build_query(key_value_node):
        splits = [ct.value.split(":") for ct in key_value_node.children]
        cleansed = [(s[0].replace("\"", "").strip(), s[1].replace("\"", "").strip()) for s in splits]
        return ' & '.join([f'{c[0]} == "{c[1]}"' for c in cleansed])

    def _apply_when_row(self, node) -> Tuple[str, bool]:
        q = self._build_query(node.children[0]) # key value pairs
        qualifying_rows = self._obj.query(q)
        target_columns = node.children[1]
        target_columns_values = [ct.value.split("==") for ct in target_columns.children]
        cleansed_target_columns_values = [(s[0].replace("\"", "").strip(), s[1].replace("\"", "").strip()) for s in target_columns_values]
        
        for c in cleansed_target_columns_values:
            unique_values = qualifying_rows[c[0]].unique()
            if not (len(unique_values) == 1 and unique_values[0] == c[1]):
                return (f'{node.data}: Column {c[0]} does not pass', False)
        return (node.data, True)

    def _apply_check(self, check) -> Tuple[str, bool]:
        try:
            c = check[0]
            if c.data == "row_count":
                comparator = c.children[0]
                quantity = int(c.children[1])
                return c.data, self._comparator_to_fn(comparator, quantity)(self._obj.shape[0])
            elif c.data == "has_columns":
                return self._apply_has_columns(c)
            elif c.data == "is_unique":
                column_name = self._treat_column_name(c.children[0])
                return c.data, self._obj[column_name].is_unique
            elif c.data == "not_null":
                column_name = self._treat_column_name(c.children[0])
                return c.data, self._obj[column_name].isna().sum() == 0
            elif c.data == "is_positive":
                column_name = self._treat_column_name(c.children[0])
                return c.data, (self._obj[column_name] > 0).all()
            elif c.data == "has_one_of":
                return self._apply_has_one_of(c)
            elif c.data == "quantile":
                return self._apply_quantile(c)
            elif c.data == "is_date":
                return self._apply_date_validation(c)
            elif c.data == "value_length":
                return self._apply_value_length(c)
            elif c.data == "percent_value_length":
                return self._apply_percent_value_length(c)
            elif c.data == "when_row_identified_by":
                return self._apply_when_row(c)
            else:
                raise GenieException(f"{c.data} seems to be not implemented in the DSL")
        except KeyError:
            return "Key error: {0} for {1}".format(c.data, c.children[0]), False
        except Exception as e:
            raise GenieException(f"{c.data} has errors: {e}")    

    def _apply_predicates(self, predicates) -> List[Tuple[str, bool]]:
        results = []
        for predicate in predicates:
            if predicate.data == "code_block":
                for check in predicate.children:
                    v = self._apply_check(check.children)
                    results.insert(0, v)
            else:
                raise GenieException('Unknown instruction: %s' % predicates.data)
        return results

    def _run(self, pt: Tree) -> List[Tuple[str, bool]]:
        if len(pt.children) != 1:
            raise GenieException('How is this possible: %s' % pt.children)

        instruction = pt.children[0]
        if instruction.data == "predicates":
            return self._apply_predicates(instruction.children)
        else:
            raise GenieException('Unknown instruction: %s' % instruction.data)

    @staticmethod
    def _parse_spec(check_spec) -> Tree:
        p = Lark(resource_string(__name__, 'data/grammar.lark').decode('utf-8'), parser='lalr')
        return p.parse(check_spec)

    @staticmethod
    def validate_spec(check_spec) -> str:
        try:
            QualityChecker._parse_spec(check_spec)
            return None, True
        except Exception as e:
            return str(e), False

    def run(self, check_spec, ignore_column_case=False):
        ast = self._parse_spec(check_spec)
        self.ignore_column_case = ignore_column_case
        if self.ignore_column_case:
            self._obj.columns = map(str.lower, self._obj.columns)

        return self._run(ast)



