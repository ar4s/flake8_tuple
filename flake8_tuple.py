# -*- coding: utf-8 -*-
__version__ = '0.1.0'

import ast


class TupleChecker(object):
    name = 'flake8-tuple'
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree

    def run(self):
        for stmt in ast.walk(self.tree):
            if not isinstance(stmt, ast.Tuple):
                continue
            if len(stmt.elts) == 1:
                yield (
                    stmt.lineno,
                    stmt.col_offset,
                    'T801 one element tuple',
                    'T801'
                )
