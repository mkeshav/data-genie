import pandas as pd
import pandas_flavor as pf
from lark import Lark, Tree
from pkg_resources import resource_string
from typing import Tuple, List
from genie_pkg import GenieException

@pf.register_dataframe_accessor('dqc')
class QualityChecker(object):
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        if obj.dropna(axis='columns').empty:
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

    def _apply_quantile(self, node) -> Tuple[str, bool]:
        column_name = node.children[0]
        q = float(node.children[1])
        c = node.children[2]
        rhs = float(node.children[3])
        lhs = self._obj[column_name].quantile(q)
        return node.data, self._comparator_to_fn(c, rhs)(lhs)

    def _apply_date_validation(self, node) -> Tuple[str, bool]:
        column_name = node.children[0]
        try:
            pd.to_datetime(self._obj[column_name])
            return node.data, True
        except Exception as _:
            return "Parse error: {0} for {1}".format(node.data, node.children[0]), False

    def _apply_has_one_of(self, node) -> Tuple[str, bool]:
        column_name = node.children[0]
        allowed_values = [ct.value.replace("\"", "") for ct in node.children[1].children]
        unique_values = self._obj[column_name].unique()
        return node.data, all(elem in allowed_values for elem in unique_values)

    def _apply_check(self, check) -> Tuple[str, bool]:
        try:
            c = check[0]
            if c.data == "has_size":
                quantity = int(c.children[0])
                return c.data, self._obj.shape[0] == quantity
            elif c.data == "has_columns":
                column_names = [ct.value.replace("\"", "") for ct in c.children[0].children]
                return c.data, len(set(self._obj.columns).intersection(column_names)) == len(column_names)
            elif c.data == "is_unique":
                column_name = c.children[0]
                return c.data, self._obj[column_name].is_unique
            elif c.data == "not_null":
                column_name = c.children[0]
                return c.data, self._obj[column_name].isna().sum() == 0
            elif c.data == "is_positive":
                column_name = c.children[0]
                return c.data, (self._obj[column_name] > 0).all()
            elif c.data == "has_one_of":
                return self._apply_has_one_of(c)
            elif c.data == "quantile":
                return self._apply_quantile(c)
            elif c.data == "is_date":
                return self._apply_date_validation(c)
            else:
                raise GenieException(f"{c.data} seems to be not implemented in the DSL")
        except KeyError:
            return "Key error: {0} for {1}".format(c.data, c.children[0]), False

    def _apply_predicates(self, predicates) -> List[Tuple[str, bool]]:
        results = []
        for predicate in predicates:
            if predicate.data == "code_block":
                for check in predicate.children:
                    v = self._apply_check(check.children)
                    results.insert(0, v)
            else:
                raise SyntaxError('Unknown instruction: %s' % predicates.data)
        return results


    def _run(self, pt: Tree) -> List[Tuple[str, bool]]:
        for instruction in pt.children:
            if instruction.data == "predicates":
                return self._apply_predicates(instruction.children)
            else:
                raise SyntaxError('Unknown instruction: %s' % instruction.data)


    @staticmethod
    def _parse(check_spec) -> Tree:
        p = Lark(resource_string(__name__, 'data/grammar.g').decode('utf-8'))
        return p.parse(check_spec)


    def run(self, check_spec):
        ast = self._parse(check_spec)
        return self._run(ast)



