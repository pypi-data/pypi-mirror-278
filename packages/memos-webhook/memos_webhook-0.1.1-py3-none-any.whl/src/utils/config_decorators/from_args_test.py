import unittest
from typing import TypedDict

from .from_args import to_args_key


class ToArgsKeyTestCase(TypedDict):
    input: str
    want: str


class TestToArgsKey(unittest.TestCase):
    def test_to_args_key(self):
        cases: list[ToArgsKeyTestCase] = [
            {"input": "field_name_of_one_class", "want": "field-name-of-one-class"},
            {"input": "fieldNameOfOneClass", "want": "field-name-of-one-class"},
            {"input": "FieldNameOfOneClass", "want": "field-name-of-one-class"},
            {"input": "SOME_VALUE", "want": "some-value"},
            {"input": "ANOTHER_VALUE", "want": "another-value"},
        ]

        for c in cases:
            got = to_args_key(c["input"])
            self.assertEqual(
                got, c["want"], f"input: {c['input']}, want: {c['want']}, got: {got}"
            )
