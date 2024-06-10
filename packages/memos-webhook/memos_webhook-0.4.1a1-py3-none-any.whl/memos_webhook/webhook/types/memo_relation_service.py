from enum import IntEnum

from pydantic import BaseModel, Field


class MemosRelation_Type(IntEnum):
    UNSPECIFIED = 0
    REFERENCE = 1
    COMMENT = 2


class MemoRelation(BaseModel):
    memo: str = ""
    related_memo: str = ""
    type: MemosRelation_Type = MemosRelation_Type.UNSPECIFIED
