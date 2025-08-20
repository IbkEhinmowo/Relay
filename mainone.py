from Core.inputAdapters.InputEvent import Event
from Core.Processor.LLMAGENT import llmagent_process

def main():
    """Main entry point for the Relay application"""
    # Create a test event
    event = Event()
    event.message = "What's the weather in Lagos, Nigeria?"
    
    # Process the event with the LLM agent
    response = llmagent_process(event)
    
    # Print the response
    print(f"Response: {response}")

if __name__ == "__main__":
    main()
