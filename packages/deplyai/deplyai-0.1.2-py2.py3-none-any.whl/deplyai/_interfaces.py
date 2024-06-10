from typing import Optional, TypedDict, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class ThreadStatus(Enum):
    UNTHREADED = 1
    THREAD_PARENT = 2
    THREAD_CHILD = 3

class InstantMessageReaction(BaseModel):
    name: str
    count: int
    users: List[str]
    parent: float

class EditedStatus(BaseModel):
    user: str
    ts: datetime

class InstantMessageFile(BaseModel):
    user: str # The user ID belonging to the user that incited this action.
    team: str
    channel: str
    internal_tenant: str

    file_name: str
    file_size: int
    ts: datetime
    file_url: str
    platform: str

class InstantMessage(BaseModel):
    platform: str # slack, teams, etc
    event_id: str # specific to the platform

    user: str # The user ID belonging to the user that incited this action.
    user_friendly_name: str # User's friendly name
    team: str
    channel: str
    channel_friendly_name: str

    text: str
    ts: str
    attachments: Optional[List[InstantMessageFile]] = None
    thread_ts: Optional[float] = None
    thread_status: ThreadStatus = ThreadStatus.UNTHREADED
    edited: Optional[EditedStatus] = None
    hidden: bool = False
    deleted: Optional[datetime] = None
    reactions: Optional[List[InstantMessageReaction]] = None



class MessagingInterface:
    """Defines the standard operations required for messaging platforms."""

    def parse_raw_message(self, raw_message: dict) -> InstantMessage:
        """Parses the incoming raw message to a structured internal representation."""
        raise NotImplementedError

    def parse_raw_react(self, raw_react: dict) -> InstantMessage:
        """Parses the incoming raw react to a structured internal representation."""
        raise NotImplementedError

    def parse_file_shared(self, raw_file_event: dict) -> InstantMessageFile:
        raise NotImplementedError

    def send_message(self, message: InstantMessage):
        """Sends a message using the platform's messaging API."""
        raise NotImplementedError

    def send_reaction(self, message_id: str, reaction_type: str):
        """Sends a reaction to a message based on its ID and the reaction type."""
        raise NotImplementedError

    def delete_message(self, message_id: str):
        """Deletes a message based on its ID."""
        raise NotImplementedError

    def edit_message(self, message_id: str, new_text: str):
        """Edits an existing message."""
        raise NotImplementedError