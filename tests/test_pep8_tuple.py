# -*- coding: utf-8 -*-
import ast
import unittest

from ddt import ddt, data, unpack

from flake8_tuple import TupleChecker


def _create_checker(code):
    return TupleChecker(ast.parse(code), 'test.py')


@ddt
class Testflake8Tuple(unittest.TestCase):
    @unpack
    @data(
        ("foo = 1,", 1),
        ("foo = 1", 0),
        ("bar = 1; foo = bar,", 1),
        ("foo = (\n3,\n4,\n)", 0),
    )
    def test_tuple(self, code, errors):
        checker = _create_checker(code)
        self.assertEqual(len(list(checker.run())), errors)
