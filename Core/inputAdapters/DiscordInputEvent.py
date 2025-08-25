
class DiscordInputEvent:
    def __init__(self, user_id: str, content: str, username: str = None, quoted_content: str = None, message_history: list = None):
        self.user_id = user_id
        self.content = content
        self.username = username
        self.quoted_content = quoted_content
        self.message_history = message_history if message_history is not None else []

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
            prompt += "\n--- End History ---"
        prompt += f"\n{self.content}"
        return prompt
