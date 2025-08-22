from Core.Processor.ToolSet import mcp
from Core.Processor.LLMAGENT import llmagent_process
import sys

def main():
    result = llmagent_process("update notion page with the words i love you 999 and get the weather in new york")
    print(result)

if __name__ == "__main__":
    main()