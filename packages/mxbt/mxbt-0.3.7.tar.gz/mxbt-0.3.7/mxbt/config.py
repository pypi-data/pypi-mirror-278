from nio.crypto import ENCRYPTION_ENABLED
from dataclasses import dataclass, field
from typing import Dict
import dotenv
import json
import os

@dataclass
class Config:
    
    encryption_enabled: bool = ENCRYPTION_ENABLED
    ignore_unverified_devices: bool = True 
    emoji_verify: bool = False
    join_on_invite: bool = True
    prefix: str = "!"
    selfbot: bool = False

    data: Dict=field(
        default_factory=lambda: dict()
    )

    @classmethod
    def from_json(cls, path: str) -> "Config":
        """
        Initialize class using JSON file.
        You can provide any custom options with format:
            {
                'name' : value
            }
        """
        return cls(
            json.load(open(path, mode='r'))
        )

    @classmethod
    def from_env(cls, filepath: str=".env", **kwargs) -> "Config":
        """
        Initialize class using .env file.
        You can provide any custom options with format:
            name = ENV_VAR_NAME
        """
        dotenv.load_dotenv(filepath)
        data = dict()
        for key, value in kwargs.items():
            data[key] = os.environ.get(value)
        return cls(**data)


