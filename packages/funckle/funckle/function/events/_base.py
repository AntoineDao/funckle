from typing import ClassVar
import flask
from pydantic import BaseModel

class SpeckleEvent(BaseModel):
    event_name: str
    data: dict


class WebhookPayload(BaseModel):
    streamId: str
    userId: str
    activityMessage: str = None
    event: SpeckleEvent

class RequestPayload(BaseModel):
    payload: WebhookPayload
            

class EventData(BaseModel):
    event_type: ClassVar[str] = "commit_create"

    @classmethod
    def from_webhook_payload(cls, payload: WebhookPayload):
        if payload.event.event_name == cls.event_name:
            return cls(**payload.event.data)
        else:
            raise ValueError(f"Event name {payload.event.event_name} does not match {cls.event_name}")
