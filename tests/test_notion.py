import os
import sys
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Core.Integrations.Notion import NotionIntegration

load_dotenv()

def test_notion_integration():
    """
    Tests the Notion integration by initializing the client and updating a page.
    """
    print("--- Starting Notion Integration Test ---")
    
    api_key = os.getenv("NOTION_API_KEY")
    page_id = os.getenv("NOTION_PAGE_ID")

    if not api_key:
        print("ERROR: NOTION_API_KEY not found")
        return
    
    if not page_id:
        print("ERROR: NOTION_PAGE_ID not found")
        return

    print(f"Found NOTION_PAGE_ID: {page_id}")

    try:
        # Initialize NotionIntegration
        notion_client = NotionIntegration()
        
        # Test updating a page
        test_string = "Hello from the test script!"
        print(f"Attempting to create page with title: '{test_string}'")
        result = notion_client.create_subpage(test_string, "This is a test body.")
        print(f"SUCCESS: {result}")
        delete = notion_client.delete_page(result)
        print(f"Cleanup: {delete}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("--- Notion Integration Test Finished ---")

if __name__ == "__main__":
    test_notion_integration()
