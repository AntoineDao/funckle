from typing import Optional
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='funckle_')  
    
    user_token: Optional[str] = None
    webhook_secret: Optional[str] = None
    speckle_host: str = 'speckle.xyz'

    def speckle_client(self):
        from specklepy.api.client import SpeckleClient
        client = SpeckleClient(host=self.speckle_host)
        client.authenticate(token=self.user_token)
        return client

settings = Settings()