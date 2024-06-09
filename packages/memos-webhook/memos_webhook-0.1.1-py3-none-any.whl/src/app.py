from __future__ import print_function

import asyncio
import contextlib
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI

import proto.gen.memos.api.v1 as v1
from src.dependencies.config import get_config, new_config
from src.dependencies.memos_cli import MemosCli, get_memos_cli, new_memos_cli
from src.dependencies.plugin_manager import (get_plugin_executor,
                                             new_plugin_executor)
from src.plugins.base_plugin import PluginExecutor
from src.plugins.you_get_plugin import YouGetPlugin
from src.utils.logger import logger as util_logger
from src.utils.logger import logging_config
from src.webhook.types.webhook_payload import WebhookPayload

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
    payload: WebhookPayload,
    executor: PluginExecutor,
):
    await executor.execute(payload)


@app.post("/webhook")
async def webhook_hanlder(
    payload: WebhookPayload,
    background_tasks: BackgroundTasks,
    executor: Annotated[PluginExecutor, Depends(get_plugin_executor)],
):
    # 添加后台任务
    background_tasks.add_task(webhook_task, payload, executor)
    return {
        "code": 0,
        "message": f"Task started in background with param: {payload.model_dump_json()}",
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
