from Core.inputAdapters.InputEvent import Event
from datetime import datetime

def discord_to_event(raw: dict) -> Event:
    """
    Convert raw Discord message data to a normalized Event instance.
    """
    return Event(
            source="discord",
            type="message",
            content=raw.get("content", ""),
        )
raw = {
    "channel_id": "654321",
    "channel_name": "general",
    "content": "Hello, world!",
    "attachments": []
}
event = discord_to_event(raw)
print(event)
