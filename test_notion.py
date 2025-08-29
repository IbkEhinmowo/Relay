import os
from Core.Integrations.Notion import NotionIntegration
from dotenv import load_dotenv

# Load environment variables from .env file in the root directory
load_dotenv()

# Check if environment variables are loaded
api_key = os.getenv("NOTION_API_KEY")
page_id = os.getenv("NOTION_PAGE_ID")

if not api_key:
    print("ERROR: NOTION_API_KEY not found. Make sure it's set in your .env file.")
    should_run_tests = False
elif not page_id:
    print("ERROR: NOTION_PAGE_ID not found. Make sure it's set in your .env file.")
    should_run_tests = False
else:
    should_run_tests = True
    print(f"Found NOTION_PAGE_ID: {page_id}")

# Initialize NotionIntegration globally if credentials are available
notion_client = NotionIntegration() if should_run_tests else None

def test_notion_integration():
    """
    Tests the Notion integration by initializing the client and updating a page.
    """
    if not should_run_tests:
        return
        
    print("--- Starting Notion Integration Test ---")
    
    try:
        # # Test updating a page
        # test_string = "Hello from the test dddddddscript!"
        # print(f"Attempting to update page with title: '{test_string}'")
        # result = notion_client.update_page(test_string)
        # print(f"SUCCESS: {result}")
        
        # Test creating a subpage
        print("\n--- Testing Subpage Creation ---")
        heading = "Test Subpage"
        body = "This is a test subpage created from the test script."
        print(f"Attempting to create subpage with heading: '{heading}'")
        subpage_result = notion_client.create_subpage(heading, body)
        print(f"SUCCESS: {subpage_result}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("--- Notion Integration Test Finished ---")

def test_create_subpage():
    """
    Tests only the subpage creation functionality of the Notion integration.
    """
    if not should_run_tests:
        return
        
    print("--- Starting Notion Subpage Creation Test ---")
    
    try:
        # Test creating a subpage
        heading = "Test Subpage " + os.getenv("TEST_RUN_ID", str(os.urandom(4).hex()))
        body = "This is a test subpage created at " + os.getenv("TEST_TIME", "current time") + "."
        print(f"Attempting to create subpage with heading: '{heading}'")
        result = notion_client.create_subpage(heading, body)
        print(f"SUCCESS: {result}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("--- Notion Subpage Creation Test Finished ---")

if __name__ == "__main__":
    # Choose which test to run - uncomment the one you want
    test_notion_integration()
    # test_create_subpage()

if __name__ == "__main__":
    # Choose which test to run - uncomment the one you want
    test_notion_integration()
    # test_create_subpage()
