import pytest

from models.provider import Provider


@pytest.fixture
def mock_provider():
    """Single mock provider for simple tests."""
    return Provider(
        url="https://eth-mainnet.test.com", name="Test Provider", type="http"
    )


@pytest.fixture
def mock_providers():
    """List of mock providers for testing provider switching."""
    return [
        Provider(url="https://provider1.test.com", name="Provider1", type="http"),
        Provider(url="https://provider2.test.com", name="Provider2", type="http"),
    ]


@pytest.fixture
def mock_block_data():
    """Mock block data for testing."""
    return {
        "number": 12345,
        "timestamp": 1678901234,
        "transactions": ["tx1", "tx2", "tx3"],
        "hash": "0x123...",
        "parentHash": "0x456...",
        "miner": "0x789...",
        "gasLimit": 15000000,
        "gasUsed": 12000000,
    }
