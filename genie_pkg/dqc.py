import pandas as pd
import pandas_flavor as pf
from lark import Lark, Tree, Token
from pkg_resources import resource_string
from typing import Tuple, List, Any
from genie_pkg import GenieException
import numpy as np
from dateutil.parser import parse


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

    def _treat_column_name(self, column_name: Token) -> str:
        if self.ignore_column_case:
            return column_name.value.lower()
        return column_name.value

    def _apply_quantile(self, node) -> Tuple[str, Any, bool]:
        column_name = self._treat_column_name(node.children[0])
        q = float(node.children[1])
        c = node.children[2]
        rhs = float(node.children[3])
        lhs = self._obj[column_name].quantile(q)
        return node.data, column_name, self._comparator_to_fn(c, rhs)(lhs)

    @staticmethod
    def _is_date(datestr):
        try:
            parse(datestr)
            return True
        except ValueError:
            return False
        
    
    @staticmethod
    def _str_to_bool(boolstr):
        if boolstr == 'True':
            return True
        return False

    def _apply_date_validation(self, node) -> Tuple[str, Any, bool]:
        column_name = self._treat_column_name(node.children[0])
        pass_percent = 100
        ignore_nulls = False
        if len(node.children) == 3:
            pass_percent = int(node.children[1])
            ignore_nulls = self._str_to_bool(node.children[2])

        if len(node.children) == 2:
            c = node.children[1]
            if c.type == 'PERCENT':
                pass_percent = int(c.value)
            if c.type == 'BOOL':
                ignore_nulls = self._str_to_bool(c.value)


        non_null_rows = self._obj[self._obj[column_name].notnull()]
        valid_dates = non_null_rows[non_null_rows[column_name].apply(self._is_date)]
        if not ignore_nulls:
            return node.data, column_name, (valid_dates.shape[0]/self._obj.shape[0])*100 >= pass_percent
        else:
            if (non_null_rows.shape[0] > 0):
                return node.data, column_name, (valid_dates.shape[0]/non_null_rows.shape[0])*100 >= pass_percent

        return node.data, column_name, False


    def _apply_has_one_of(self, node) -> Tuple[str, Any, bool]:
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

        return node.data, column_name, all(elem in allowed_values for elem in unique_values)

    def _apply_percent_value_length(self, node) -> Tuple[str, Any, bool]:
        column_name = self._treat_column_name(node.children[0])
        pass_percent = 100
        ignore_nulls = False
        if len(node.children) == 4:
            # index 2 is "=="
            c = node.children[1]
            if c.type == 'PERCENT':
                pass_percent = int(c.value)
            if c.type == 'BOOL':
                ignore_nulls = self._str_to_bool(c.value)
            print('here...')                
            rhs = int(node.children[3])
        elif len(node.children) == 3:
            # index 1 is "=="
            rhs = int(node.children[2])
        else:
            pass_percent = int(node.children[1])
            ignore_nulls = node.children[2]
            # index 3 is "=="
            rhs = int(node.children[4])

        self._obj['length'] = self._obj[column_name].fillna('').astype(str).map(len)
        if ignore_nulls == 'True':
            not_na_df = self._obj.replace(r'^\s*$', np.NaN, regex=True).dropna()
        else:
            not_na_df = self._obj

        passing = not_na_df[not_na_df['length'] == rhs]
        if not ignore_nulls:
            return node.data, column_name, (passing.shape[0]/self._obj.shape[0])*100 >= pass_percent
        else:
            if (not_na_df.shape[0] > 0):
                return node.data, column_name, (passing.shape[0]/not_na_df.shape[0])*100 >= pass_percent
        
        return node.data, column_name, False

    def _apply_has_columns(self, node) -> Tuple[str, Any, bool]:
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

        return node.data, ','.join(columns_in_df), len(set(columns_in_df).intersection(expected_columns)) == len(set(expected_columns))

    @staticmethod
    def _build_query(key_value_node: Tree):
        splits = [ct.value.split(":") for ct in key_value_node.children]
        cleansed = [(s[0].replace("\"", "").strip(), s[1].replace("\"", "").strip()) for s in splits]
        return ' & '.join([f'{c[0]} == "{c[1]}"' for c in cleansed])

    def _apply_when_row(self, node) -> Tuple[str, Any, bool]:
        q = self._build_query(node.children[0]) # key value pairs
        qualifying_rows = self._obj.query(q)
        target_columns = node.children[1]
        target_columns_values = [ct.value.split("==") for ct in target_columns.children]
        cleansed_target_columns_values = [(s[0].replace("\"", "").strip(), s[1].replace("\"", "").strip()) for s in target_columns_values]
        
        for c in cleansed_target_columns_values:
            unique_values = qualifying_rows[c[0]].unique()
            if not (len(unique_values) == 1 and unique_values[0] == c[1]):
                return (f'{node.data}: Column {c[0]} does not pass', 'None', False)
        return node.data, None, True

    def _apply_check(self, check) -> Tuple[str, Any, bool]:
        try:
            c = check[0]
            if c.data == "row_count":
                comparator = c.children[0]
                quantity = int(c.children[1])
                return c.data, None, self._comparator_to_fn(comparator, quantity)(self._obj.shape[0])
            elif c.data == "has_columns":
                return self._apply_has_columns(c)
            elif c.data == "is_unique":
                column_name = self._treat_column_name(c.children[0])
                return c.data, None, self._obj[column_name].is_unique
            elif c.data == "not_null":
                column_name = self._treat_column_name(c.children[0])
                return c.data, None, self._obj[column_name].isna().sum() == 0
            elif c.data == "is_positive":
                column_name = self._treat_column_name(c.children[0])
                return c.data, column_name, (self._obj[column_name] > 0).all()
            elif c.data == "has_one_of":
                return self._apply_has_one_of(c)
            elif c.data == "quantile":
                return self._apply_quantile(c)
            elif c.data == "is_date":
                return self._apply_date_validation(c)
            elif c.data == "percent_value_length":
                return self._apply_percent_value_length(c)
            elif c.data == "when_row_identified_by":
                return self._apply_when_row(c)
            else:
                raise GenieException(f"{c.data} seems to be not implemented in the DSL")
        except KeyError:
            return "Key error: {0} for {1}".format(c.data, c.children[0]), None, False
        except Exception as e:
            raise GenieException(f"{c.data} has errors: {e}")    

    def _apply_predicates(self, predicates) -> List[Tuple[str, Any, bool]]:
        results:List[Tuple[str, Any, bool]] = []
        for predicate in predicates:
            if predicate.data == "code_block":
                for check in predicate.children:
                    v = self._apply_check(check.children)
                    results.insert(0, v)
            else:
                raise GenieException('Unknown instruction: %s' % predicates.data)
        return results

    def _run(self, pt: Tree) -> List[Tuple[str, Any, bool]]:
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
    def validate_spec(check_spec) -> Tuple[Any, bool]:
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



