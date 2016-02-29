# -*- coding: utf-8 -*-
__version__ = '0.2.2'

import ast
import token
import tokenize


ERROR_CODE = 'T801'
ERROR_MESSAGE = 'one element tuple'


class TupleChecker(object):
    name = 'flake8-tuple'
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def run(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
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
        token[2][0]
        for token in tokens
        if (
            token[0] == tokenize.COMMENT and
            (
                token[1].endswith('noqa') or
                (
                    isinstance(token[0], str) and token[0].endswith('noqa')
                )
            )
        )]
    return noqa


def check_code_for_wrong_tuple(code):
    tree = ast.parse(code)
    code = code.split("\n")
    noqa = get_noqa_lines(code)
    return check_for_wrong_tuple(tree, code, noqa)


def check_for_wrong_tuple(tree, code, noqa):
    errors = []
    candidates = []
    for assign in ast.walk(tree):
        if not isinstance(assign, ast.Assign) or assign.lineno in noqa:
            continue
        for tuple_el in ast.walk(assign):
            if isinstance(tuple_el, ast.Tuple) and len(tuple_el.elts) == 1:
                candidates.append((assign.lineno, assign.col_offset))
                break
    if not candidates:
        return []
    for candidate in candidates:
        tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
        for t in tokens:
            if t.start[0] == candidate[0] and t.start[1] >= candidate[1]:
                while t.type != token.OP and t.string != '=':
                    t = next(tokens)
                t = next(tokens)
                if t.type != token.OP and t.string != '(' and t.type != token.ENDMARKER:
                    errors.append(t.start)
                    t = next(tokens)
    return errors
