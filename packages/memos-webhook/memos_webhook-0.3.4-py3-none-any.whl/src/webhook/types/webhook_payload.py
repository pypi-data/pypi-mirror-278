from pydantic import BaseModel, Field

from .memo_service import Memo


class WebhookPayload(BaseModel):
    """WebhookPayload is the payload of webhook request.

    https://github.com/usememos/memos/blob/main/plugin/webhook/webhook.go
    """

    url: str = ""
    activityType: str = ""
    creatorId: int = 0
    createdTs: int = 0
    memo: Memo | None = None
