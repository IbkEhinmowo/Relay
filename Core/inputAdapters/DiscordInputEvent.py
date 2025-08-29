
class DiscordInputEvent:
    def __init__(self, user_id: str, content: str, username: str = None, quoted_content: str = None, message_history: list = None, tool_response: list = None):
        self.user_id = user_id
        self.content = content
        self.username = username
        self.quoted_content = quoted_content
        self.message_history = message_history if message_history is not None else []
        self.tool_response = tool_response if tool_response is not None else []

    def to_prompt(self):
        # Standardize the prompt format for the LLM
        prompt = f"[USER_ID: {self.user_id}]"
        if self.username:
            prompt += f" [USERNAME: {self.username}]"
        if self.quoted_content:
            prompt += f"\n> {self.quoted_content}"
        if self.message_history:
            prompt += "\n--- Conversation History ---"
            for msg in self.message_history:
                prompt += f"\n{msg}"
            prompt += "\n--- End History ---  ---"
        if self.tool_response:
            prompt += "\n--- Recent Tool Activity ---"
            for response in self.tool_response:
                prompt += f"\n{response}"
            prompt += "\n--- End Tool Activity --- NOW RESPOND TO THE NEW MESSAGE BELOW ---"
        prompt += f"\n{self.content}"
        return prompt
