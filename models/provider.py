from typing import Literal

from pydantic import BaseModel, Field


class Provider(BaseModel):
    url: str = Field(..., description="Provider API endpoint URL")
    type: Literal["http", "websocket"] = Field(
        default="http", description="Connection type"
    )
    name: str = Field(..., description="Human-readable provider name")
