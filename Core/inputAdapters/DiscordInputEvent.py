class DiscordInputEvent:
    def __init__(self, user_id: str, content: str, username: str = None, quoted_content: str = None):
        self.user_id = user_id
        self.content = content
        self.username = username
        self.quoted_content = quoted_content

    def to_prompt(self):
        # Standardize the prompt format for the LLM
        prompt = f"[USER_ID: {self.user_id}]"
        if self.username:
            prompt += f" [USERNAME: {self.username}]"
        if self.quoted_content:
            prompt += f"\n> {self.quoted_content}"
        prompt += f"\n{self.content}"
        return prompt
