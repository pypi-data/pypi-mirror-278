from typing import TypedDict, Optional, List, Union

from ..enums import PubSubMessageEventNameEnum, MessageSenderTypeEnum, MessageStatusEnum


class MessageUserType(TypedDict, total=False):
    id: str
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    avatar: Optional[str]


class MessageAgentType(TypedDict, total=False):
    id: str
    name: Optional[str]
    email: Optional[str]


class RecordingType(TypedDict, total=False):
    id: str
    duration_seconds: int


class AttachmentType(TypedDict, total=False):
    id: int
    size_bytes: float


class MessageRecordingType(TypedDict, total=False):
    url: Optional[str]
    duration_seconds: Optional[int]


class MessageAttachmentType(TypedDict, total=False):
    url: str
    size_bytes: int


class PubsubMessageEventType(TypedDict, total=False):
    timestamp: Optional[str]
    user: MessageUserType
    message_id: str
    sender_type: MessageSenderTypeEnum
    agent: Optional[MessageAgentType]
    call_center_phone: Optional[str]
    text: Optional[str]
    conversation_link: Optional[str]
    recording: Optional[MessageRecordingType]
    note: Optional[str]
    hangup_cause: Optional[str]
    charge_fee: Optional[float]
    attachments: Optional[List[MessageAttachmentType]]
    campaign_id: Optional[str]
    campaign_name: Optional[str]


class PubsubMessageStatusEventType(TypedDict, total=False):
    timestamp: Optional[str]
    message_id: str
    status: MessageStatusEnum


class PubsubMessageType(TypedDict, total=False):
    access_token: str
    organization_id: str
    installed_source_id: int
    source_id: str
    source: str
    event_name: PubSubMessageEventNameEnum
    data: Union[PubsubMessageEventType, PubsubMessageStatusEventType]
