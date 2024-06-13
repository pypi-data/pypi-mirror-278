from datetime import datetime

import memos_webhook.proto_gen.memos.api.v1 as v1

from .types.common import RowStatus as OldRowStatus
from .types.google_protobuf import PbTimestamp as OldPbTimestamp
from .types.memo_relation_service import MemoRelation as OldRelation
from .types.memo_service import Memo as OldMemo
from .types.memo_service import Visibility as OldVisibility
from .types.resource_service import Resource as OldResource
from .types.webhook_payload import WebhookPayload as OldPayload


def old_row_status_to_proto(row_status: OldRowStatus) -> v1.RowStatus:
    return v1.RowStatus(int(row_status))


def old_timestamp_to_proto(timestamp: OldPbTimestamp | None) -> datetime:
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp.seconds + (timestamp.nanos) * 0.001)


def old_visibility_to_proto(visibility: OldVisibility) -> v1.Visibility:
    return v1.Visibility(int(visibility))


def old_resource_to_proto(input: OldResource) -> v1.Resource:
    return v1.Resource(
        name=input.name,
        uid=input.uid,
        create_time=input.create_time,
        filename=input.filename,
        content=input.content,
        external_link=input.external_link,
        type=input.type,
        size=input.size,
        memo=input.memo,
    )


def old_relation_to_proto(input: OldRelation) -> v1.MemoRelation:
    return v1.MemoRelation(
        memo=input.memo,
        related_memo=input.related_memo,
        type=v1.MemoRelationType(int(input.type)),
    )


def old_memo_to_proto(input: OldMemo) -> v1.Memo:
    return v1.Memo(
        name=input.name,
        uid=input.uid,
        row_status=old_row_status_to_proto(input.row_status),
        creator=input.creator,
        create_time=old_timestamp_to_proto(input.create_time),
        update_time=old_timestamp_to_proto(input.update_time),
        display_time=old_timestamp_to_proto(input.display_time),
        content=input.content,
        nodes=[],  # we do not handle nodes transformation for old version.
        visibility=old_visibility_to_proto(input.visibility),
        tags=input.tags,
        pinned=input.pinned,
        parent_id=input.parent_id,
        resources=[old_resource_to_proto(resource) for resource in input.resources],
        relations=[old_relation_to_proto(relation) for relation in input.relations],
        parent=input.parent,
    )


def old_payload_to_proto(input: OldPayload) -> v1.WebhookRequestPayload:
    return v1.WebhookRequestPayload(
        url=input.url,
        activity_type=input.activityType,
        creator_id=input.creatorId,
        create_time=datetime.fromtimestamp(input.createdTs),
        memo=old_memo_to_proto(input.memo),
    )
