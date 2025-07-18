from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional

class EmailDict(TypedDict):
    id: str
    subject: str
    sender: str
    body: str


class EmailAssistantState(TypedDict):
    user_input: str
    emails: List[EmailDict]
    current_email: Optional[EmailDict]
    summaries: List[str]
    replies: List[str]
    messages: List
    user_wants_reply: Optional[bool]

