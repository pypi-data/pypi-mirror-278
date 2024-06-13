from pydantic import BaseModel, Field


class PbTimestamp(BaseModel):
    seconds: int = 0
    nanos: int = 0
