from typing import ClassVar, List, Union
from pydantic import BaseModel

from ._base import EventData

class StreamRecord(BaseModel):
    id: str
    name: str
    description: str = None
    isPublic: bool
    clonedFrom: str = None
    createdAt: str
    updatedAt: str
    allowPublicComments: bool
    isDiscoverable: bool

class StreamUpdateInput(BaseModel):
    id: str
    allowPublicComments: bool = None
    description: str = None
    isDiscoverable: bool = None
    isPublic: bool = None
    name: str = None


class StreamUpdated(EventData):
    event_type: ClassVar[str] = "stream_update"

    old: StreamRecord
    new: StreamUpdateInput

class StreamCloned(EventData):
    event_type: ClassVar[str] = "stream_clone"

    sourceStreamId: str
    newStreamId: str 
    clonerId: str

class StreamPermissionAdded(EventData):
    event_type: ClassVar[str] = "stream_permissions_add"

    targetUser: str
    role: str

class StreamInvitationAccepted(EventData):
    event_type: ClassVar[str] = "stream_permissions_invite_accepted"

    inviterUser: str
    role: str

class StreamPermissionRemoved(EventData):
    event_type: ClassVar[str] = "stream_permissions_remove"

    targetUser: str

class StreamInviteSent(EventData):
    event_type: ClassVar[str] = "stream_invite_sent"

    targetId: str = None
    targetEmail: str = None

class StreamInviteDeclined(EventData):
    event_type: ClassVar[str] = "stream_invite_declined"

    targetId: str
    inviterId: str 