from enum import IntEnum

from pydantic import BaseModel, Field


class Reaction_Type(IntEnum):
    TYPE_UNSPECIFIED = 0
    THUMBS_UP = 1
    THUMBS_DOWN = 2
    HEART = 3
    FIRE = 4
    CLAPPING_HANDS = 5
    LAUGH = 6
    OK_HAND = 7
    ROCKET = 8
    EYES = 9
    THINKING_FACE = 10
    CLOWN_FACE = 11
    QUESTION_MARK = 12


class Reaction(BaseModel):
    creator: str = ""
    content_id: str = ""
    reaction_type: Reaction_Type = Reaction_Type.TYPE_UNSPECIFIED
