import pytest
from pydantic import ValidationError

from models.block import Block
from models.provider import Provider


def test_provider_model_valid():
    provider_data = {
        "url": "https://eth-mainnet.test.com",
        "name": "Test Provider",
        "type": "http",
    }
    provider = Provider(**provider_data)
    assert provider.url == provider_data["url"]
    assert provider.name == provider_data["name"]
    assert provider.type == provider_data["type"]


def test_provider_model_invalid_type():
    provider_data = {
        "url": "https://eth-mainnet.test.com",
        "name": "Test Provider",
        "type": "invalid",  # Only http or websocket allowed
    }
    with pytest.raises(ValidationError):
        Provider(**provider_data)


def test_block_model_from_raw():
    raw_block = {
        "number": 123456,
        "timestamp": 1678901234,
        "transactions": ["tx1", "tx2", "tx3"],
        "other_field": "value",
    }

    block = Block.from_raw(raw_block)
    assert block.number == raw_block["number"]
    assert block.timestamp == raw_block["timestamp"]
    assert block.tx_count == len(raw_block["transactions"])
    assert block.raw == raw_block


def test_block_model_invalid():
    # Missing required fields
    raw_block = {
        "number": 123456,
        # Missing timestamp
        "transactions": [],
    }

    with pytest.raises((ValidationError, KeyError)):
        Block.from_raw(raw_block)
