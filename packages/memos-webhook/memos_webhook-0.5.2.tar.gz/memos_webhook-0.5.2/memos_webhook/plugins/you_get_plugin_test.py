import re
import unittest
from typing import TypedDict

from .you_get_plugin import extract_urls

twitter_patterns = [
    re.compile(r"https://twitter.com/\w+/status/\d+"),
    re.compile(r"https://x.com/\w+/status/\d+"),
]


class ExtractUrlsTestCase(TypedDict):
    content: str
    want: list[str]


class TestExtractUrls(unittest.TestCase):
    def test_extract_urls(self):
        test_cases: list[ExtractUrlsTestCase] = [
            {
                "content": "Check out this tweet: https://twitter.com/user/status/123456",
                "want": ["https://twitter.com/user/status/123456"],
            },
            {
                "content": "Here is a link from x.com: https://x.com/tomeinohito/status/1796144897721835717",
                "want": ["https://x.com/tomeinohito/status/1796144897721835717"],
            },
            {"content": "No URLs in this content", "want": []},
            {
                "content": "Here have many urls: https://twitter.com/user/status/123456, https://x.com/post/status/789, Yes!",
                "want": [
                    "https://twitter.com/user/status/123456",
                    "https://x.com/post/status/789",
                ],
            },
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                self.assertEqual(
                    extract_urls(test_case["content"], twitter_patterns),
                    test_case["want"],
                )


if __name__ == "__main__":
    unittest.main()
