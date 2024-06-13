import asyncio
import mimetypes
import re
from logging import Logger
from typing import override

import aiofiles
import aiofiles.os
import betterproto.lib.google.protobuf as pb

from memos_webhook.dependencies.config import YouGetPluginConfig
from memos_webhook.dependencies.memos_cli import MemosCli
from memos_webhook.proto_gen.memos.api import v1
from memos_webhook.webhook.types.webhook_payload import WebhookPayload

from .base_plugin import BasePlugin, pluginLogger


def extract_urls(content: str, patterns: list[re.Pattern[str]]) -> list[str]:
    """Extract urls match pattern from content."""
    urls: list[str] = []
    for pattern in patterns:
        urls.extend(pattern.findall(content))
    return urls


class YouGetPlugin(BasePlugin):
    logger: Logger = pluginLogger.getChild("YouGetPlugin")
    cfg: YouGetPluginConfig
    patterns: list[re.Pattern[str]]

    def __init__(self, cfg: YouGetPluginConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.patterns = [re.compile(pattern) for pattern in cfg.patterns]

    def activity_types(self) -> list[str]:
        return ["memos.memo.created", "memos.memo.updated"]

    @override
    def tag(self) -> str:
        return self.cfg.tag

    @override
    def additional_trigger(self, payload: v1.WebhookRequestPayload) -> bool:
        urls = extract_urls(payload.memo.content, self.patterns)
        if urls:
            return True
        return False

    @override
    async def task(
        self, payload: v1.WebhookRequestPayload, memos_cli: MemosCli
    ) -> v1.Memo:
        memo_name = payload.memo.name
        self.logger.info(f"Start {self.cfg.name} webhook task for memo: {memo_name}")

        # list memo resources
        list_res_resp = await memos_cli.memo_service.list_memo_resources(
            v1.ListMemoResourcesRequest(name=memo_name)
        )
        remote_resources = list_res_resp.resources  # resources already in memo
        self.logger.info(
            f"Memo resources existed: {[res.name for res in remote_resources]}"
        )

        # extract urls
        urls = extract_urls(payload.memo.content, self.patterns)
        if not urls:
            self.logger.info("No urls found")
            return payload.memo
        self.logger.info(f"Extracted urls: {urls}")

        # mkdir
        download_to = f"./download/{memo_name}"
        await aiofiles.os.makedirs(download_to, exist_ok=True)

        self.logger.info(f"Download to: {download_to}")

        # you-get
        for url in urls:
            command = ["you-get", "-o", download_to, url]
            process = await asyncio.create_subprocess_exec(
                *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                self.logger.error(f"Error executing you-get: {stderr.decode()}")
            else:
                self.logger.info(f"Download successful: {stdout.decode()}")

        # create resource
        filenames = await aiofiles.os.listdir(download_to)

        self.logger.info(f"Files in {download_to}: {filenames}")

        # filter already downloaded files
        filenames = list(
            set(filenames) - set([res.filename for res in remote_resources])
        )
        self.logger.info(f"Files to be uploaded: {filenames}")

        uploaded_resources: list[v1.Resource] = []
        for filename in filenames:
            async with aiofiles.open(f"{download_to}/{filename}", "rb") as f:
                res = await memos_cli.resource_service.create_resource(
                    v1.CreateResourceRequest(
                        resource=v1.Resource(
                            filename=filename,
                            content=await f.read(),
                            type=mimetypes.guess_type(filename)[0]
                            or "application/octet-stream",
                        )
                    )
                )
            uploaded_resources.append(res)

        self.logger.info(
            f"Create resource response: {[res.name for res in uploaded_resources]}"
        )

        # set memo resources, will not trigger update memo event
        all_resources = remote_resources + uploaded_resources
        await memos_cli.memo_service.set_memo_resources(
            v1.SetMemoResourcesRequest(name=memo_name, resources=all_resources)
        )
        self.logger.info(f"Set memo resources: {[res.name for res in all_resources]}")

        return payload.memo  # you-get plugin do not modify memo content
