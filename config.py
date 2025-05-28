import ast
import json

from pydantic import Field, field_validator
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

    @field_validator("channel_ids", mode="before")
    @classmethod
    def parse_channel_ids(cls, v):
        if isinstance(v, list):
            return [str(x) for x in v]
        if isinstance(v, str):
            try:
                return [str(x) for x in json.loads(v)]
            except Exception:
                try:
                    return [str(x) for x in ast.literal_eval(v)]
                except Exception:
                    return []
        return []
