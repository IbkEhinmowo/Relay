from Core.Processor.ToolSet import mcp
from Core.Processor.LLMAGENT import llmagent_process
import sys

def main():
    result = llmagent_process("get weather data for vancouver and send it to discord")
    print(result)

if __name__ == "__main__":
    main()