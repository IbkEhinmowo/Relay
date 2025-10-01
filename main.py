import os
import json
import requests
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras
from groq import Groq


load_dotenv()

grok_api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=grok_api_key)
completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
      {
        "role": "user",
        "content": ""
      }
    ],
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None,
    tools=[{"type":"browser_search"}]
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")



