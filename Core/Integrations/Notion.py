import os
from notion_client import Client
from dotenv import load_dotenv

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
    def __init__(self):
        load_dotenv()
        self.notion = Client(auth=os.getenv("NOTION_API_KEY"))
        self.page_id = Client(auth=os.getenv("NOTION_PAGE_ID"))  # your target page

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
    