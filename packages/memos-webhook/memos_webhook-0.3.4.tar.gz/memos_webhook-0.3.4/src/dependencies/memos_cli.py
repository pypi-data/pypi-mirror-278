import contextlib
from dataclasses import dataclass

from grpclib.client import Channel

import proto.gen.memos.api.v1 as v1
from src.utils.logger import logger as util_logger

from .config import Config

logger = util_logger.getChild("memos_cli")


@dataclass
class MemosCli:
    memo_service: v1.MemoServiceStub
    resource_service: v1.ResourceServiceStub


_cli: MemosCli = None


@contextlib.contextmanager
def new_memos_cli(cfg: Config):
    global _cli
    logger.debug(f"create channel on {cfg.memos_host}:{cfg.memos_port}")

    metadata = {"authorization": f"Bearer {cfg.memos_token}"}
    try:
        channel = Channel(cfg.memos_host, cfg.memos_port)
        memo_service = v1.MemoServiceStub(channel, metadata=metadata)
        resource_service = v1.ResourceServiceStub(channel, metadata=metadata)
        _cli = MemosCli(memo_service, resource_service)
        logger.debug("channel created")
        yield _cli
    finally:
        channel.close()
        _cli = None


def get_memos_cli():
    assert _cli is not None, "memos_cli not initialized"
    return _cli
