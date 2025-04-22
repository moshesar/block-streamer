from pydantic import BaseModel, Field


class Block(BaseModel):
    number: int
    timestamp: int
    tx_count: int = Field(..., description="The amount of transactions")
    raw: dict = Field(..., description="The raw block data returned by the provider")

    @classmethod
    def from_raw(cls, raw_block: dict) -> "Block":
        return cls(
            number=raw_block["number"],
            timestamp=raw_block["timestamp"],
            tx_count=len(raw_block.get("transactions", [])),
            raw=raw_block,
        )
