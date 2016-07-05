# -*- coding: utf-8 -*-
import ast
import collections
import six
import token
import tokenize

from flake8.engine import pep8

__version__ = '0.2.11'


ERROR_CODE = 'T801'
ERROR_MESSAGE = 'one element tuple'


if six.PY2:
    """
    Backported from Python 3.x
    """
    TokenInfo = collections.namedtuple(
        'TokenInfo', ['type', 'string', 'start', 'end', 'line']
    )
else:
    TokenInfo = tokenize.TokenInfo


def get_lines(filename):
    if filename in ('stdin', '-', None):
        return pep8.stdin_get_value().splitlines(True)
    else:
        return pep8.readlines(filename)


class TupleChecker(object):
    name = 'flake8-tuple'
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def run(self):
        try:
            lines = get_lines(self.filename)
        except IOError:
            yield
        noqa = get_noqa_lines(lines)

        for error in check_for_wrong_tuple(self.tree, lines, noqa):
            yield (
                error[0],
                error[1],
                ('{} {}').format(ERROR_CODE, ERROR_MESSAGE),
                type(self)
            )


def get_noqa_lines(code):
    tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
    noqa = [
        x[2][0]
        for x in tokens
        if (
            x[0] == tokenize.COMMENT and
            (
                x[1].endswith('noqa') or
                (
                    isinstance(x[0], str) and x[0].endswith('noqa')
                )
            )
        )]
    return noqa


def check_code_for_wrong_tuple(code):
    tree = ast.parse(code)
    code = [line + '\n' for line in code.split('\n')]
    noqa = get_noqa_lines(code)
    return check_for_wrong_tuple(tree, code, noqa)


def check_for_wrong_tuple(tree, code, noqa):
    errors = []
    candidates = []
    for assign in ast.walk(tree):
        if not isinstance(assign, ast.Assign) or assign.lineno in noqa:
            continue
        elif isinstance(assign.value, ast.Call):
            continue
        for tuple_el in ast.walk(assign):
            if isinstance(tuple_el, ast.Tuple) and len(tuple_el.elts) == 1:
                candidates.append((assign.lineno, assign.col_offset))
                break
    if not candidates:
        return []
    for candidate in candidates:
        tokens = tokenize.generate_tokens(
            lambda L=iter(code): next(L)
        )
        for t in tokens:
            x = TokenInfo(*t)
            if x.start[0] != candidate[0]:
                continue
            if x.type == token.OP and x.string == '=':
                x = TokenInfo(*next(tokens))
                if x.type != token.OP and x.string != '(':
                    x_next = TokenInfo(*next(tokens))
                    if x_next.type == token.OP and x_next.string == ',':
                        errors.append(x.start)
    return errors
