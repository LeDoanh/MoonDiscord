from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Dict


class Config(BaseSettings):
    discord_token: str = Field(..., alias="DISCORD_TOKEN")
    status: str = Field(default=None, alias="DISCORD_STATUS")
    instructions: str = Field(default=None, alias="INSTRUCTIONS")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_base_url: str = Field(..., alias="OPENAI_BASE_URL")
    openai_model: str = Field(default="gpt-5-mini", alias="OPENAI_MODEL")

    # Models and token limits loaded from environment
    premium_models: set[str] = Field(default_factory=set, alias="PREMIUM_MODELS")
    mini_models: set[str] = Field(default_factory=set, alias="MINI_MODELS")
    token_limits: Dict[str, int] = Field(default_factory=dict, alias="TOKEN_LIMITS")
    token_usage_file: str = Field(default="token_usage.json", alias="TOKEN_USAGE_FILE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
