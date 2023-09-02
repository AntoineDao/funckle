from typing import ClassVar
from ._base import EventData

class StreamAccessRequestSent(EventData):
    event_type: ClassVar[str] = "stream_access_request_sent"
    requesterId: str


class StreamAccessRequestDeclined(EventData):
    event_type: ClassVar[str] = "stream_access_request_declined"
    requesterId: str
    declinerId: str
