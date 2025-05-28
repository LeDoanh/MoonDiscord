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
        if not v:
            return []
        if isinstance(v, list):
            return [str(x) for x in v]
        if isinstance(v, str):
            v = v.strip()
            # Try comma-separated first (fastest for .env usage)
            if "," in v and not (v.startswith("[") and v.endswith("]")):
                return [s.strip() for s in v.split(",") if s.strip()]
            # Try JSON
            try:
                data = json.loads(v)
                if isinstance(data, list):
                    return [str(x) for x in data]
            except Exception:
                pass
            # Try Python literal
            try:
                data = ast.literal_eval(v)
                if isinstance(data, list):
                    return [str(x) for x in data]
            except Exception:
                pass
        return []
