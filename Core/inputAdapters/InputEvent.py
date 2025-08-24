from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict
from datetime import datetime

class Event(BaseModel):
    # Common fields for all sources
    source: str               # "discord", "marketplace", "email"
    type: Optional[str] = None # "message", "task", "listing"
    content: str              # Main text/content of the event
    timestamp: Optional[str] = None
    sender: Optional[str] = None
    priority: Optional[str] = None   # e.g., "critical", "high", "medium", "low"
    
    # Optional metadata for source-specific info
    metadata: Optional[Dict[str, str]] = None

# # Examples of mapping:

# # Discord message
# discord_event = Event(
#     source="discord",
#     type="message",
#     content="Server down in region 1",
#     timestamp=datetime.utcnow(),
#     sender="AdminUser",
#     metadata={"channel": "alerts"}
# )

# # Marketplace listing
# marketplace_event = Event(
#     source="marketplace",
#     type="listing",
#     content="RTX 4090 for sale",
#     timestamp=datetime.utcnow(),
#     metadata={"price": "700", "url": "https://example.com/listing", "category": "GPU"}
# )

# # Email
# email_event = Event(
#     source="email",
#     type="task",
#     content="Please review the Q3 report",
#     timestamp=datetime.utcnow(),
#     sender="boss@example.com",
#     metadata={"folder": "inbox"}
# )