from abc import ABC, abstractmethod
from logging import Logger
from typing import Protocol

import betterproto.lib.google.protobuf as pb

from proto.gen.memos.api import v1
from src.dependencies.memos_cli import MemosCli
from src.utils.logger import logger
from src.webhook.types.webhook_payload import WebhookPayload

pluginLogger = logger.getChild("plugin")


class PluginProtocol(Protocol):
    """The protocol that plugin executor trully need a plugin to implement.
    
    You should implement `BasePlugin` instead of this protocol.
    Unless you know what you are doing."""
    def positive_tag(self) -> str: ...
    def negative_tag(self) -> str: ...
    async def task(self, payload: WebhookPayload, memos_cli: MemosCli) -> v1.Memo: ...
    def should_trigger(self, payload: WebhookPayload) -> bool: ...


class BasePlugin(PluginProtocol, ABC):
    """The abstract class for webhook plugin.

    DO NOT extend this class more than two levels.
    Use composition instead of inheritance."""

    logger = pluginLogger.getChild("BasePlugin")

    @abstractmethod
    def activity_types(self) -> list[str]:
        """The trigger events for the webhook plugin.

        The task will be triggered by the events in the list.
        And will never be triggered by the events not in the list.

        Valid events:
        - `memos.memo.created`
        - `memos.memo.updated`
        - `memos.memo.deleted`
        """
        ...

    @abstractmethod
    def tag(self) -> str:
        """Tag for the webhook plugin focus on.

        The task will be triggered by memos with `#tag`.
        And will never be triggered by memos with `#tag/done`.

        We also call `#tag/done` as a `negative tag`.

        Once the task triggered, will replace the `#tag` with `#tag/done`.
        If the `#tag` not exists, will add the `#tag/done` to first line.
        """
        ...

    @abstractmethod
    async def task(self, payload: WebhookPayload, memos_cli: MemosCli) -> v1.Memo:
        """The webhook task function.

        Return the modified memo, and the plugin will auto update the memo with modified content and negative tag.

        Never update the memo content in the task function.
        Let the executor do the update.
        Or the memo could be updated multiple times by different plugins and cause unexpected behavior.
        """
        ...

    def positive_tag(self) -> str:
        """The positive tag for the webhook plugin."""
        return f"#{self.tag()}"

    def negative_tag(self) -> str:
        """The negative tag for the webhook plugin."""
        return f"#{self.tag()}/done"

    def additional_trigger(self, payload: WebhookPayload) -> bool:
        """The additional trigger besides the tag.
        If return True and negative tag not exists,
        the webhook will be triggered even if the tag not exists.
        """
        return False

    def should_trigger(self, payload: WebhookPayload) -> bool:
        """Check if the rule should trigger by the payload.

        First check if the payload activity type is in the trigger activity types.
        Then check (not negative_tag && (positive_tag || additional_trigger)).

        Not suppose to be override. Or you should well implement the negative condition logic.
        """
        assert payload.memo is not None, "payload memo is None"

        if payload.activityType not in self.activity_types():
            self.logger.info(f"activityType not match: {payload.activityType}")
            return False

        negative_tag, positive_tag = self.negative_tag(), self.positive_tag()
        self.logger.info(f"negative_tag: {negative_tag}, positive_tag: {positive_tag}")

        if self.negative_tag() in payload.memo.content:
            self.logger.info(f"memos matched negative, tag: {negative_tag}")
            return False

        if self.positive_tag() in payload.memo.content:
            self.logger.info(f"memos matched positive, tag: {positive_tag}")
            return True

        if self.additional_trigger(payload):
            self.logger.info(f"additional trigger matched")
            return True

        self.logger.info(f"memos not matched")
        return False


class PluginExecutor:
    """The class responsible for execute one plugin for one payload."""

    plugins: list[PluginProtocol]
    memos_cli: MemosCli
    logger: Logger

    def __init__(self, memos_cli: MemosCli, plugins: list[PluginProtocol]) -> None:
        self.memos_cli = memos_cli
        self.plugins = plugins
        self.logger = logger.getChild("PluginExecutor")

    async def update_memo_content(
        self, plugin: PluginProtocol, payload: WebhookPayload
    ) -> v1.Memo:
        """update memo content
        Once the task triggered, will replace the `#tag` with `#tag/done`.
        If the `#tag` not exists, will add the `#tag/done` to first line.
        """
        self.logger.debug(
            f"Background task started with param: {payload.model_dump_json()}"
        )

        res_memo = await plugin.task(payload, self.memos_cli)
        self.logger.info("Background task success completed")

        # update memo
        if plugin.positive_tag() in res_memo.content:
            res_memo.content = res_memo.content.replace(
                plugin.positive_tag(), plugin.negative_tag()
            )
        else:
            res_memo.content = f"{plugin.negative_tag()}\n{res_memo.content}"

        updated_memo = await self.memos_cli.memo_service.update_memo(
            v1.UpdateMemoRequest(
                memo=res_memo,
                update_mask=pb.FieldMask(paths=["content"]),
            )
        )
        self.logger.debug(f"Updated memo content {updated_memo.content}")

    async def execute(self, payload: WebhookPayload) -> None:
        """Execute the webhook task by the rule."""
        for plugin in self.plugins:
            self.logger.info(f"Execute plugin: {plugin}")
            if not plugin.should_trigger(payload):
                continue

            await self.update_memo_content(plugin, payload)

        self.logger.info("All plugins executed")
