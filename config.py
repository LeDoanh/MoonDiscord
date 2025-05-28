import ast

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    discord_token: str = Field(..., alias="DISCORD_TOKEN")
    channel_ids: list[str] = Field(default_factory=list, alias="DISCORD_CHANNEL_IDS")
    status: str = Field(default=None, alias="DISCORD_STATUS")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_base_url: str = Field(..., alias="OPENAI_BASE_URL")
    openai_model: str = Field(default="gpt-4o", alias="OPENAI_MODEL")
    openai_instructions: str = Field(default=None, alias="OPENAI_INSTRUCTIONS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __init__(self, **values):
        super().__init__(**values)
        # Parse channel_ids from string if needed (handle JSON/decode errors gracefully)
        if isinstance(self.channel_ids, str):
            try:
                import json

                self.channel_ids = [str(x) for x in json.loads(self.channel_ids)]
            except Exception:
                try:
                    self.channel_ids = [
                        str(x) for x in ast.literal_eval(self.channel_ids)
                    ]
                except Exception:
                    self.channel_ids = []
