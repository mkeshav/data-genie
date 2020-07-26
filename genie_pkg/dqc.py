import pandas as pd
import pandas_flavor as pf
from lark import Lark, Tree
from pkg_resources import resource_string

@pf.register_dataframe_accessor('dqc')
class QualityChecker(object):
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        if obj.dropna(axis='columns').empty:
            raise AttributeError("DataFrame is empty!!! What quality do you expect from emptiness")

    def _apply_check(self, check):
        try:
            c = check[0]
            if c.data == "has_size":
                quantity = int(c.children[0])
                return c.data, self._obj.shape[0] == quantity
            elif c.data == "has_columns":
                column_names = []
                for ct in c.children[0].children:
                    name = ct.value
                    column_names.insert(0, name.replace("'", ""))
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
            else:
                return c.data, False
        except KeyError:
            return "Key error: {0} for {1}".format(c.data, c.children[0]), False

    def _apply_predicates(self, predicates):
        results = []
        for predicate in predicates:
            if predicate.data == "code_block":
                for check in predicate.children:
                    v = self._apply_check(check.children)
                    results.insert(0, v)
            else:
                raise SyntaxError('Unknown instruction: %s' % predicates.data)
        return results


    def _run(self, pt: Tree):
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



