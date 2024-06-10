from __future__ import annotations

from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel, Field

from .google_protobuf import PbTimestamp


class LineBreakNode(BaseModel):
    pass


class ParagraphNode(BaseModel):
    children: List[Node] = []


class CodeBlockNode(BaseModel):
    language: str = ""
    code: str = ""


class HeadingNode(BaseModel):
    level: int = 0
    children: List[Node] = []


class HorizontalRuleNode(BaseModel):
    symbol: str = ""


class BlockquoteNode(BaseModel):
    children: List[Node] = []


class OrderedListNode(BaseModel):
    number: str = ""
    indent: int = 0
    children: List[Node] = []


class UnorderedListNode(BaseModel):
    symbol: str = ""
    indent: int = 0
    children: List[Node] = []


class TaskListNode(BaseModel):
    symbol: str = ""
    indent: int = 0
    complete: bool = False
    children: List[Node] = []


class MathBlockNode(BaseModel):
    content: str = ""


class TableNode_Row(BaseModel):
    cells: List[str] = []


class TableNode(BaseModel):
    header: List[str] = []
    delimiter: List[str] = []
    rows: List[TableNode_Row] = []


class EmbeddedContentNode(BaseModel):
    resource_name: str = ""
    params: str = ""


class TextNode(BaseModel):
    content: str = ""


class BoldNode(BaseModel):
    symbol: str = ""
    children: List[Node] = []


class ItalicNode(BaseModel):
    symbol: str = ""
    content: str = ""


class BoldItalicNode(BaseModel):
    symbol: str = ""
    content: str = ""


class CodeNode(BaseModel):
    content: str = ""


class ImageNode(BaseModel):
    alt_text: str = ""
    url: str = ""


class LinkNode(BaseModel):
    text: str = ""
    url: str = ""


class AutoLinkNode(BaseModel):
    url: str = ""
    is_raw_text: bool = False


class TagNode(BaseModel):
    content: str = ""


class StrikethroughNode(BaseModel):
    content: str = ""


class EscapingCharacterNode(BaseModel):
    symbol: str = ""


class MathNode(BaseModel):
    content: str = ""


class HighlightNode(BaseModel):
    content: str = ""


class SubscriptNode(BaseModel):
    content: str = ""


class SuperscriptNode(BaseModel):
    content: str = ""


class ReferencedContentNode(BaseModel):
    resource_name: str = ""
    params: str = ""


class SpoilerNode(BaseModel):
    content: str = ""


class OneOfNode(BaseModel):
    lineBreakNode: LineBreakNode | None = Field(alias="LineBreakNode", default=None)
    paragraphNode: ParagraphNode | None = Field(alias="ParagraphNode", default=None)
    codeBlockNode: CodeBlockNode | None = Field(alias="CodeBlockNode", default=None)
    headingNode: HeadingNode | None = Field(alias="HeadingNode", default=None)
    horizontalRuleNode: HorizontalRuleNode | None = Field(
        alias="HorizontalRuleNode", default=None
    )
    blockquoteNode: BlockquoteNode | None = Field(alias="BlockquoteNode", default=None)
    orderedListNode: OrderedListNode | None = Field(
        alias="OrderedListNode", default=None
    )
    unorderedListNode: UnorderedListNode | None = Field(
        alias="UnorderedListNode", default=None
    )
    taskListNode: TaskListNode | None = Field(alias="TaskListNode", default=None)
    mathBlockNode: MathBlockNode | None = Field(alias="MathBlockNode", default=None)
    tableNode: TableNode | None = Field(alias="TableNode", default=None)
    embeddedContentNode: EmbeddedContentNode | None = Field(
        alias="EmbeddedContentNode", default=None
    )
    textNode: TextNode | None = Field(alias="TextNode", default=None)
    boldNode: BoldNode | None = Field(alias="BoldNode", default=None)
    italicNode: ItalicNode | None = Field(alias="ItalicNode", default=None)
    boldItalicNode: BoldItalicNode | None = Field(alias="BoldItalicNode", default=None)
    codeNode: CodeNode | None = Field(alias="CodeNode", default=None)
    imageNode: ImageNode | None = Field(alias="ImageNode", default=None)
    linkNode: LinkNode | None = Field(alias="LinkNode", default=None)
    autoLinkNode: AutoLinkNode | None = Field(alias="AutoLinkNode", default=None)
    tagNode: TagNode | None = Field(alias="TagNode", default=None)
    strikethroughNode: StrikethroughNode | None = Field(
        alias="StrikethroughNode", default=None
    )
    escapingCharacterNode: EscapingCharacterNode | None = Field(
        alias="EscapingCharacterNode", default=None
    )
    mathNode: MathNode | None = Field(alias="MathNode", default=None)
    highlightNode: HighlightNode | None = Field(alias="HighlightNode", default=None)
    subscriptNode: SubscriptNode | None = Field(alias="SubscriptNode", default=None)
    superscriptNode: SuperscriptNode | None = Field(
        alias="SuperscriptNode", default=None
    )
    referencedContentNode: ReferencedContentNode | None = Field(
        alias="ReferencedContentNode", default=None
    )
    spoilerNode: SpoilerNode | None = Field(alias="SpoilerNode", default=None)


class NodeType(IntEnum):
    NODE_UNSPECIFIED = 0
    LINE_BREAK = 1
    PARAGRAPH = 2
    CODE_BLOCK = 3
    HEADING = 4
    HORIZONTAL_RULE = 5
    BLOCKQUOTE = 6
    ORDERED_LIST = 7
    UNORDERED_LIST = 8
    TASK_LIST = 9
    MATH_BLOCK = 10
    TABLE = 11
    EMBEDDED_CONTENT = 12
    TEXT = 13
    BOLD = 14
    ITALIC = 15
    BOLD_ITALIC = 16
    CODE = 17
    IMAGE = 18
    LINK = 19
    AUTO_LINK = 20
    TAG = 21
    STRIKETHROUGH = 22
    ESCAPING_CHARACTER = 23
    MATH = 24
    HIGHLIGHT = 25
    SUBSCRIPT = 26
    SUPERSCRIPT = 27
    REFERENCED_CONTENT = 28
    SPOILER = 29


class Node(BaseModel):
    type: NodeType = NodeType.NODE_UNSPECIFIED
    Node: OneOfNode | None = None


LineBreakNode.model_rebuild()
ParagraphNode.model_rebuild()
CodeBlockNode.model_rebuild()
HeadingNode.model_rebuild()
HorizontalRuleNode.model_rebuild()
BlockquoteNode.model_rebuild()
OrderedListNode.model_rebuild()
UnorderedListNode.model_rebuild()
TaskListNode.model_rebuild()
MathBlockNode.model_rebuild()
TableNode_Row.model_rebuild()
TableNode.model_rebuild()
EmbeddedContentNode.model_rebuild()
TextNode.model_rebuild()
BoldNode.model_rebuild()
ItalicNode.model_rebuild()
BoldItalicNode.model_rebuild()
CodeNode.model_rebuild()
ImageNode.model_rebuild()
LinkNode.model_rebuild()
AutoLinkNode.model_rebuild()
TagNode.model_rebuild()
StrikethroughNode.model_rebuild()
EscapingCharacterNode.model_rebuild()
MathNode.model_rebuild()
HighlightNode.model_rebuild()
SubscriptNode.model_rebuild()
SuperscriptNode.model_rebuild()
ReferencedContentNode.model_rebuild()
SpoilerNode.model_rebuild()
OneOfNode.model_rebuild()
Node.model_rebuild()
