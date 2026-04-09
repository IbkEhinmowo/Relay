from Core.Processor.LLMAGENT import llmagent_process
import asyncio

def main():
    """Main entry point for the Relay application"""
    # Create a test event
 
    message = "What's the weather in Lagos, Nigeria?"
    
    # Process the event with the LLM agent
    response = asyncio.run(llmagent_process(message))
    
    # Print the response
    print(f"Response: {response}")

if __name__ == "__main__":
    main()
