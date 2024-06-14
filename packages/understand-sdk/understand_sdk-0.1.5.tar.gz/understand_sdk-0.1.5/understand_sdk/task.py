from typing import Any, Dict, Optional

from pydantic import Field

from understand_sdk.model import BaseModel


class ConnectionConfig(BaseModel):
    version: int
    data: Dict[str, Any]


class Connection(BaseModel):
    type: str
    provider: str
    config: Optional[ConnectionConfig] = None


class Workspace(BaseModel):
    id: str
    slug: str


class Channel(BaseModel):
    id: str
    slug: str


class Task(BaseModel):
    id: str
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    workspace: Workspace
    channel: Channel
    connection: Connection


class Event(BaseModel):
    group: str = "container"
    name: str
    value: str
