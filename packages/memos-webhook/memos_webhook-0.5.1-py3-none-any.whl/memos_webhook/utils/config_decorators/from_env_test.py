import unittest
from typing import TypedDict

from .from_env import to_env_key


class ToEnvKeyTestCase(TypedDict):
    input: str
    want: str


class TestToEnvKey(unittest.TestCase):
    def test_to_env_key(self):
        cases: list[ToEnvKeyTestCase] = [
            {"input": "field_name_of_one_class", "want": "FIELD_NAME_OF_ONE_CLASS"},
            {"input": "fieldNameOfOneClass", "want": "FIELD_NAME_OF_ONE_CLASS"},
            {"input": "FieldNameOfOneClass", "want": "FIELD_NAME_OF_ONE_CLASS"},
            {"input": "someValue", "want": "SOME_VALUE"},
            {"input": "anotherValue", "want": "ANOTHER_VALUE"},
        ]

        for c in cases:
            got = to_env_key(c["input"])
            self.assertEqual(
                got, c["want"], f"input: {c['input']}, want: {c['want']}, got: {got}"
            )
