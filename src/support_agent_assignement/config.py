from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_aws import ChatBedrockConverse 
from botocore.config import Config

config=Config(
    retries={
        "max_attempts": 10,
        "mode": "adaptive"
    }
)

class Settings(BaseSettings):
    helpdesk_base_url: str
    api_key: str
    candidate_email: str
    aws_access_key_id: str
    aws_secret_access_key: str  
    aws_region_name: str
    
    vector_db_path: str = "./data/chroma"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().with_name(".env"),
        extra="ignore",
    )


settings = Settings()




def get_bedrock_llm():
   return ChatBedrockConverse(
   region_name=settings.aws_region_name,
   temperature=0,
   model="us.anthropic.claude-opus-4-5-20251101-v1:0",
   aws_access_key_id=settings.aws_access_key_id,
   aws_secret_access_key=settings.aws_secret_access_key,
   config=config,
   
   
   )