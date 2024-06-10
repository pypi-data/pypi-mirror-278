from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel, Field

from .common import RowStatus
from .google_protobuf import PbTimestamp
from .markdown_service import Node
from .memo_relation_service import MemoRelation
from .reaction import Reaction
from .resource_service import Resource


class Visibility(IntEnum):
    VISIBILITY_UNSPECIFIED = 0
    PRIVATE = 1
    PROTECTED = 2
    PUBLIC = 3


class MemoProperty(BaseModel):
    tags: List[str] = []
    has_link: bool = False
    has_task_list: bool = False
    has_code: bool = False


class Memo(BaseModel):
    """pb generated memo struct json marshal

    https://github.com/usememos/memos/blob/main/proto/api/v1/memo_service.proto
    """

    name: str = ""
    uid: str = ""
    row_status: RowStatus = RowStatus.ROW_STATUS_UNSPECIFIED
    creator: str = ""
    create_time: PbTimestamp | None = None
    update_time: PbTimestamp | None = None
    display_time: PbTimestamp | None = None
    content: str = ""
    nodes: List[Node] = []  # TODO
    visibility: Visibility = Visibility.VISIBILITY_UNSPECIFIED
    tags: List[str] = []
    pinned: bool = False
    parent_id: int | None = None
    resources: List[Resource] = []
    relations: List[MemoRelation] = []
    reactions: List[Reaction] = []
    property: MemoProperty | None = None
    parent: str | None = None
