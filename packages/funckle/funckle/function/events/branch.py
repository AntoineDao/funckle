from typing import ClassVar, List, Union
from pydantic import BaseModel
from ._base import EventData

class BranchRecord(BaseModel):
    id: str
    streamId: str
    authorId: str
    name: str
    description: str = None
    createdAt: str
    updatedAt: str

class DeleteModelInput(BaseModel):
    id: str
    name: str
    projectId: str

class BranchDeleteInput(BaseModel):
    id: str
    name: str
    streamId: str

class BranchCreate(EventData):
    event_type: ClassVar[str] = "branch_create"

    branch: BranchRecord

class BranchUpdate(EventData):
    event_type: ClassVar[str] = "branch_update"

    old: BranchRecord
    new: BranchRecord

class BranchDelete(EventData):
    event_type: ClassVar[str] = "branch_delete"

    branch: Union[DeleteModelInput, BranchDeleteInput]