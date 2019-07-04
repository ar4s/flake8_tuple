# -*- coding: utf-8 -*-
import ast
import collections
import six
import token
import tokenize

try:
    import pycodestyle as pep8
except ImportError:
    import pep8

try:
    from flake8.engine import pep8 as stdin_utils
except ImportError:
    from flake8 import utils as stdin_utils

__version__ = '0.4.0'


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
        return stdin_utils.stdin_get_value().splitlines(True)
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


def ending_of_bad_tuple(x):
    return x.type == token.OP and x.string == ','


def check_for_wrong_tuple(tree, code, noqa):
    errors = []
    candidates = []
    for assign in ast.walk(tree):
        if (not isinstance(assign, ast.Assign) and
            not isinstance(assign, ast.Return)):
            continue
        elif assign.lineno in noqa:
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
        number_nl = 0  # account for logical newlines within statements
        tokens = tokenize.generate_tokens(
            lambda L=iter(code): next(L)
        )
        previous_token = None
        for t in tokens:
            if previous_token is not None and previous_token.type == tokenize.NEWLINE:
                number_nl = 0
            x = TokenInfo(*t)
            if x.start[0] - number_nl != candidate[0]:
                previous_token = x
                continue
            if x.type == tokenize.NL:
                number_nl += 1
            if x.type == token.NEWLINE and ending_of_bad_tuple(previous_token):
                errors.append(x.start)
            if x.type == token.OP and x.string == '=':
                x = TokenInfo(*next(tokens))
                if x.type != token.OP and x.string != '(':
                    x_next = TokenInfo(*next(tokens))
                    if ending_of_bad_tuple(x_next):
                        errors.append(x.start)
            previous_token = x
    return errors
