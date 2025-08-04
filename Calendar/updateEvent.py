from langchain_core.tools import tool


@tool
def update_calendar_event_tool(event_id: str, updates: dict) -> str:
    """
    Updates an existing calendar event.

    Parameters:
    - event_id: The unique ID of the event to update.
    - updates: A dictionary of fields to update (e.g., {'summary': 'New title', 'start': {...}}).

    Returns:
    - A success message or an error message if the update fails.
    """