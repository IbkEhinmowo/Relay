import os
from notion_client import Client


class NotionIntegration:
    def __init__(self):
        token = os.environ.get("NOTION_API_KEY")
        self.notion = Client(auth=token)
        self.page_id = os.environ.get("NOTION_PAGE_ID")

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
        return new_page['id']
    
    
    def delete_page(self, page_id: str):
        """Archive (delete) a Notion page by its ID. Use only for testing/cleanup."""
        self.notion.pages.update(page_id=page_id, archived=True)
        return f"Page {page_id} archived (deleted)."
    
    def read_page(self, page_id: str):
        """Read a Notion page's properties and content blocks."""
        page = self.notion.pages.retrieve(page_id=page_id)
        blocks = self.notion.blocks.children.list(block_id=page_id)
        return {
            "page": page,
            "blocks": blocks
        }
    

    # def create_database_page(self, database_id: str, heading: str, body: str):
    #     """Create a new page in a database (table) with a heading and body."""
    #     new_page = self.notion.pages.create(
    #         parent={"database_id": database_id},
    #         properties={
    #             "title": {
    #                 "title": [
    #                     {"text": {"content": heading}}
    #                 ]
    #             }
    #         },
    #         children=[
    #             {
    #                 "object": "block",
    #                 "type": "heading_1",
    #                 "heading_1": {"rich_text": [{"type": "text", "text": {"content": heading}}]}
    #             },
    #             {
    #                 "object": "block",
    #                 "type": "paragraph",
    #                 "paragraph": {"rich_text": [{"type": "text", "text": {"content": body}}]}
    #             }
    #         ]
    #     )
    #     return f"Created database page: {new_page['id']}"

    # def update_page_body(self, page_id: str, heading: str, body: str):
    #     """Update a page's content with a new heading and body (replaces children blocks)."""
    #     # Notion API does not support replacing all children in one call, so you may need to delete old blocks first for a true replace.
    #     # Here, we just append new blocks.
    #     new_blocks = [
    #         {
    #             "object": "block",
    #             "type": "heading_1",
    #             "heading_1": {"rich_text": [{"type": "text", "text": {"content": heading}}]}
    #         },
    #         {
    #             "object": "block",
    #             "type": "paragraph",
    #             "paragraph": {"rich_text": [{"type": "text", "text": {"content": body}}]}
    #         }
    #     ]
    #     for block in new_blocks:
    #         self.notion.blocks.children.append(page_id, children=[block])
    #     return f"Updated page {page_id} with new heading and body."

    # def update_page(self, written_string: str):
    #     """Update a Notion page with a new title."""
    #     updated_page = self.notion.pages.update(
    #         page_id=self.page_id,
    #         properties={
    #             "title": {
    #                 "title": [
    #                     {
    #                         "text": {
    #                             "content": written_string
    #                         }
    #                     }
    #                 ]
    #             }
    #         }
    #     )
    #     return f"page updated: {updated_page}"

    