from __future__ import print_function

import asyncio
import contextlib
from typing import Annotated, Any

from fastapi import BackgroundTasks, Depends, FastAPI, Request

import memos_webhook.proto_gen.memos.api.v1 as v1
from memos_webhook.dependencies.config import get_config, new_config
from memos_webhook.dependencies.memos_cli import (MemosCli, get_memos_cli,
                                                  new_memos_cli)
from memos_webhook.dependencies.plugin_manager import (get_plugin_executor,
                                                       new_plugin_executor)
from memos_webhook.plugins.base_plugin import PluginExecutor
from memos_webhook.plugins.you_get_plugin import YouGetPlugin
from memos_webhook.utils.logger import logger as util_logger
from memos_webhook.utils.logger import logging_config
from memos_webhook.webhook.type_transform import old_payload_to_proto
from memos_webhook.webhook.types.webhook_payload import WebhookPayload

logger = util_logger.getChild("app")


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.debug("webhook server started")
        cfg = get_config()
        with new_memos_cli(cfg) as memos_cli:
            executor = new_plugin_executor(cfg, memos_cli)
            yield
    finally:
        logger.info("webhook server stopped")


app = FastAPI(lifespan=lifespan)


async def webhook_task(
    payload: v1.WebhookRequestPayload,
    executor: PluginExecutor,
):
    await executor.execute(payload)


@app.post("/webhook_old")
async def webhook_old_hanlder(
    payload: WebhookPayload,
    background_tasks: BackgroundTasks,
    executor: Annotated[PluginExecutor, Depends(get_plugin_executor)],
):
    """The old webhook handler, use specific json schema."""
    # 添加后台任务
    proto_payload = old_payload_to_proto(payload)
    background_tasks.add_task(webhook_task, proto_payload, executor)
    return {
        "code": 0,
        "message": f"Task started in background with param: {payload.model_dump_json()}",
    }


@app.post("/webhook")
async def webhook_handler(
    req: Request,
    background_tasks: BackgroundTasks,
    executor: Annotated[PluginExecutor, Depends(get_plugin_executor)],
):
    """The new webhook handler, use protojson."""
    dict_json = await req.json()
    logger.debug(f"webhook handler received request: {dict_json}")
    logger.debug(f"type: {type(dict_json)}")

    proto_payload = v1.WebhookRequestPayload().from_dict(dict_json)
    background_tasks.add_task(webhook_task, proto_payload, executor)
    return {
        "code": 0,
        "message": f"Task started with param: {proto_payload.to_json()}",
    }


async def root_task(memos_cli: MemosCli):
    logger.info("root task started")
    await asyncio.sleep(3)
    res = await memos_cli.memo_service.list_memos(v1.ListMemosRequest())
    logger.info(f"list memos: {res.to_json()[:20]}")
    logger.info("root task done")


@app.get("/")
async def read_root(
    memos_cli: Annotated[MemosCli, Depends(get_memos_cli)],
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(root_task, memos_cli)
    return {"Hello": "World"}
