import os
from notion_client import Client

# Load environment variables
# load_dotenv()

# NOTION_API_KEY = os.getenv("NOTION_API_KEY")
# PAGE_ID = "256add24-7b47-80f9-9934-dc21854145fd"  # your target page

# # Initialize Notion client
# notion = Client(auth=NOTION_API_KEY)

# # Update a property (for example, a "Name" title property)
# updated_page = notion.pages.update(
#     page_id=PAGE_ID,
#     properties={
#         "title": {  # Must match the exact property name in the database
#             "title": [
#                 {
#                     "text": {
#                         "content": "Updated from Python!"
#                     }
#                 }
#             ]
#         }
#     }
# )

# print("Page updated:", updated_page['id'])


class NotionIntegration:
    def create_subpage(self, heading: str, body: str):
        """Create a new subpage (note/doc) under the main page with a heading and body."""
        new_page = self.notion.pages.create(
            parent={"page_id": self.page_id},
            properties={
                "title": {
                    "title": [
                        {"text": {"content": heading}}
                    ]
                }
            },
            children=[
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {"rich_text": [{"type": "text", "text": {"content": heading}}]}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": body}}]}
                }
            ]
        )
        return f"Created subpage: {new_page['id']}"

    def create_database_page(self, database_id: str, heading: str, body: str):
        """Create a new page in a database (table) with a heading and body."""
        new_page = self.notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "title": {
                    "title": [
                        {"text": {"content": heading}}
                    ]
                }
            },
            children=[
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {"rich_text": [{"type": "text", "text": {"content": heading}}]}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": body}}]}
                }
            ]
        )
        return f"Created database page: {new_page['id']}"

    def update_page_body(self, page_id: str, heading: str, body: str):
        """Update a page's content with a new heading and body (replaces children blocks)."""
        # Notion API does not support replacing all children in one call, so you may need to delete old blocks first for a true replace.
        # Here, we just append new blocks.
        new_blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": heading}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": body}}]}
            }
        ]
        for block in new_blocks:
            self.notion.blocks.children.append(page_id, children=[block])
        return f"Updated page {page_id} with new heading and body."
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_API_KEY"))
        self.page_id = os.getenv("NOTION_PAGE_ID")  # your target page

    def update_page(self, written_string: str):
        """Update a Notion page with a new title."""
        updated_page = self.notion.pages.update(
            page_id=self.page_id,
            properties={
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": written_string
                            }
                        }
                    ]
                }
            }
        )
        return f"page updated: {updated_page}"
    