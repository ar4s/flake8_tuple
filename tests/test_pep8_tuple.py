# -*- coding: utf-8 -*-
import unittest

from ddt import ddt, data, unpack

from flake8_tuple import check_code_for_wrong_tuple, TupleChecker


@ddt
class Testflake8Tuple(unittest.TestCase):
    @unpack
    @data(
        ("bar = 1, 2", 0),
        ("foo = 1", 0),
        ("foo = (1,)", 0),
        ("foo = 1,", 1),
        ("\nfoo = 1,", 1),
        ("\nfoo = 1,\nbar = 2,", 2),
        ("bar = 1; foo = bar,", 1),
        ("foo = (\n3,\n4,\n)\nbar = 10,", 1),
        ("foo = 3,\nbar = 10,\nfoo_bar = 2,", 3),
        ("foo = 3,\nbar = 10\nfoo_bar = 2,", 2),
        ("foo = 3,\nbar = 10,\nfoo_bar = 2",  2),  # noqa
        ("foo = 3 \nbar = 10 \nfoo_bar = 2,", 1),
        ("class A(object):\n foo = 3\n bar = 10,\n foo_bar = 2", 1),  # noqa
        ("a = ('a',)\nfrom foo import bar, baz", 0),
        ("a = ('a',)\n('b', 'c')", 0),
        ("a = ('a',)\n('b', 'c')\n", 0),
        ('"""\nfoo\n"""\nbah = 1\n', 0),
        ("base_url = reverse(\n'test',\nargs=(pk,)\n)", 0),
        ("base_url = reverse(\n'test',\nargs=pk,\n)", 0),
        ("group_by = function_call('arg'),", 1),
        ("group_by = ('foobar' * 3),", 1),
        ("val = {}.get(1),", 1),
        ("val = {}.get(\n1),", 1),
        ("def foo():\n return True, False,", 0),
        ("def foo():\n return True", 0),
        ("def foo():\n return False,", 1),
    )
    def test_tuple(self, code, errors):
        result = check_code_for_wrong_tuple(code)
        self.assertEqual(len(result), errors)

    def test_file_not_found(self):
        checker = TupleChecker(None, 'foo')
        next(checker.run())


if __name__ == '__main__':
    unittest.main()
