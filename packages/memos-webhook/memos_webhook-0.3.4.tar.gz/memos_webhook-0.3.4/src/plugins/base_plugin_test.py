import unittest
from typing import TypedDict, override

import src.webhook.types.memo_service as webhook_types
from proto.gen.memos.api import v1
from src.dependencies.memos_cli import MemosCli
from src.webhook.types.webhook_payload import WebhookPayload

from .base_plugin import BasePlugin


class MockPlugin(BasePlugin):
    @override
    def activity_types(self) -> list[str]:
        return ["memos.memo.created"]

    @override
    def tag(self) -> str:
        return "hook/download"

    @override
    async def task(self, payload: WebhookPayload, memos_cli: MemosCli) -> v1.Memo:
        return v1.Memo()


class MockOverwritePlugin(BasePlugin):
    @override
    def activity_types(self) -> list[str]:
        return ["memos.memo.created"]

    @override
    def tag(self) -> str:
        return "hook/download"
    
    @override
    def additional_trigger(self, payload: WebhookPayload) -> bool:
        if payload.memo:
            return "overwrite" in payload.memo.content
        
        return False

    @override
    async def task(self, payload: WebhookPayload, memos_cli: MemosCli) -> v1.Memo:
        return v1.Memo()


class ShouldTriggerCase(TypedDict):
    name: str
    activityType: str
    content: str
    expected: bool


class TestBasePlugin(unittest.IsolatedAsyncioTestCase):

    async def test_should_trigger(self):
        cases: list[ShouldTriggerCase] = [
            {
                "name": "should trigger",
                "activityType": "memos.memo.created",
                "content": "#hook/download",
                "expected": True,
            },
            {
                "name": "content no tag",
                "activityType": "memos.memo.created",
                "content": "hook/download",
                "expected": False,
            },
            {
                "name": "activity type not match",
                "activityType": "memos.memo.deleted",
                "content": "#hook/download",
                "expected": False,
            },
            {
                "name": "tag negative",
                "activityType": "memos.memo.created",
                "content": "#hook/download/done",
                "expected": False,
            },
        ]

        for case in cases:
            plugin = MockPlugin()
            self.assertEqual(
                plugin.should_trigger(
                    WebhookPayload(
                        activityType=case["activityType"],
                        memo=webhook_types.Memo(content=case["content"]),
                    )
                ),
                case["expected"],
                f"case({case["name"]}) failed",
            )
    
    async def test_should_trigger_overwrite(self):
        cases: list[ShouldTriggerCase] = [
            {
                "name": "should trigger with tag",
                "activityType": "memos.memo.created",
                "content": "#hook/download",
                "expected": True,
            },
            {
                "name": "should trigger with or condition",
                "activityType": "memos.memo.created",
                "content": "some overwrite",
                "expected": True,
            },
            {
                "name": "should not trigger without matched condition",
                "activityType": "memos.memo.created",
                "content": "some content",
                "expected": False,
            },
            {
                "name": "should not trigger with negative tag",
                "activityType": "memos.memo.created",
                "content": "#hook/download/done some overwrite",
                "expected": False,
            },
            {
                "name": "should not trigger with wrong activity type",
                "activityType": "memos.memo.deleted",
                "content": "some overwrite",
                "expected": False,
            }
        ]

        for case in cases:
            plugin = MockOverwritePlugin()
            self.assertEqual(
                plugin.should_trigger(
                    WebhookPayload(
                        activityType=case["activityType"],
                        memo=webhook_types.Memo(content=case["content"]),
                    )
                ),
                case["expected"],
                f"case({case["name"]}) failed",
            )
