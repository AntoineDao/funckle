from typing import ClassVar, List, Union
from pydantic import BaseModel
from ._base import EventData


class CommitRecord(BaseModel):
    id: str
    referencedObject: str
    author: str = None
    message: str = None
    createdAt: str
    sourceApplication: str = None
    totalChildrenCount: int = None
    parents: List[str] = None

class CommitUpdateInput(BaseModel):
    id: str
    message: str = None
    newBranchName: str = None
    streamId: str

class UpdateVersionInput(BaseModel):
    versionId: str
    message: str = None

class CommitCreated(EventData):
    event_type: ClassVar[str] = "commit_create"

    id: str
    projectId: str
    modelId: str
    versionId: str
    branchName: str
    message: str = None
    objectId: str
    parents: List[str] = None
    sourceApplication: str = None
    streamId: str
    totalChildrenCount: int = None

class CommitUpdated(EventData):
    event_type: ClassVar[str] = "commit_update"

    old: CommitRecord
    new: Union[CommitUpdateInput, UpdateVersionInput]

class CommitMoved(EventData):
    event_type: ClassVar[str] = "commit_move"

    originalBranchId: str
    newBranchId: str

class CommitDeleted(EventData):
    event_type: ClassVar[str] = "commit_delete"

class CommitReceived(EventData):
    event_type: ClassVar[str] = "commit_receive"

    sourceApplication: str
    message: str = None
