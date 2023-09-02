from typing import ClassVar, List, Union
from pydantic import BaseModel

from ._base import EventData

class ResourceIdentifierInput(BaseModel):
    resourceId: str
    resourceType: str

class CommentCreatedActivityInput(BaseModel):

    blobIds: List[str]
    data: dict
    resources: List[ResourceIdentifierInput] = None
    screenshot: str = None
    streamId: str
    text: dict = None

class MutationCommentArchiveArgs(BaseModel):
    commentId: str
    streamId: str
    archived: bool = None

class CommentContentInput(BaseModel):
    blodIds: List[str] = None
    doc: dict = None

class CreateCommentReplyInput(BaseModel):
    content: CommentContentInput
    threadId: str

class ReplyCreateInput(BaseModel):
    blodIds: List[str]
    data: dict = None
    parentComment: str
    streamId: str
    text: dict = None

class CommentCreated(EventData):
    event_type: ClassVar[str] = "comment_created"

    input: CommentCreatedActivityInput


class CommentArchived(EventData):
    event_type: ClassVar[str] = "comment_archived"

    input: MutationCommentArchiveArgs

class CommentReplyCreated(EventData):
    event_type: ClassVar[str] = "comment_replied"

    input: Union[CreateCommentReplyInput, ReplyCreateInput]

class CommentMentioned(EventData):
    event_type: ClassVar[str] = "comment_mention"

    mentionAuthorId: str
    mentionTargetId: str
    commentId: str
    threadId: str