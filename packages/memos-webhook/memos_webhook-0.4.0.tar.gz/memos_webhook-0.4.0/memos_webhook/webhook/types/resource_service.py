from pydantic import BaseModel, Field

from .google_protobuf import PbTimestamp


class Resource(BaseModel):
    name: str = ""
    uid: str = ""
    create_time: PbTimestamp | None = None
    filename: str = ""
    content: bytes | None = None
    external_link: str = ""
    type: str = ""
    size: int = 0
    memo: str = ""
