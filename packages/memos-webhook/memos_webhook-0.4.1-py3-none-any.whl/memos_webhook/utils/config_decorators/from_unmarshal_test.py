import unittest
from typing import TypedDict

from .from_unmarshal import to_unmarshal_key


class ToYamlKeyTestCase(TypedDict):
    input: str
    want: str


class TestToYamlKey(unittest.TestCase):
    def test_to_yaml_key(self):
        cases: list[ToYamlKeyTestCase] = [
            {"input": "field_name_of_one_class", "want": "field_name_of_one_class"},
            {"input": "fieldNameOfOneClass", "want": "field_name_of_one_class"},
            {"input": "FieldNameOfOneClass", "want": "field_name_of_one_class"},
            {"input": "SOME_VALUE", "want": "some_value"},
            {"input": "ANOTHER_VALUE", "want": "another_value"},
        ]

        for c in cases:
            got = to_unmarshal_key(c["input"])
            self.assertEqual(
                got, c["want"], f"input: {c['input']}, want: {c['want']}, got: {got}"
            )
