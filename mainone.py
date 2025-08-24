from Core.Processor.ToolSet import mcp
from Core.Processor.LLMAGENT import llmagent_process
import sys

def main():
    result = llmagent_process("get the weather in new york and update the notion page with it")
    print(result)

if __name__ == "__main__":
    main()