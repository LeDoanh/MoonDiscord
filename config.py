from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    discord_token: str = Field(..., alias="DISCORD_TOKEN")
    status: str = Field(default=None, alias="DISCORD_STATUS")
    instructions: str = Field(default=None, alias="INSTRUCTIONS")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_base_url: str = Field(..., alias="OPENAI_BASE_URL")
    openai_model: str = Field(default="gpt-5-mini", alias="OPENAI_MODEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
