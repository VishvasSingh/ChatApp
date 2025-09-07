from typing import TypedDict


class ChatInput(TypedDict):
    data: str
    isCurrentUser: bool
    timestamp: str
    userIcon: str
    username: str
