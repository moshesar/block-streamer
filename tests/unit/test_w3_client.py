from unittest.mock import Mock, patch

import pytest

from core.w3_client import W3Client
from models.provider import Provider


@pytest.fixture
def mock_provider():
    return Provider(
        url="https://eth-mainnet.test.com", name="Test Provider", type="http"
    )


@pytest.fixture
def mock_w3():
    with patch("core.w3_client.Web3") as mock:
        # Mock the Web3 instance
        w3_instance = Mock()
        mock.return_value = w3_instance

        # Mock the HTTPProvider
        mock.HTTPProvider.return_value = Mock()

        yield mock


def test_w3_client_connect_success(mock_provider, mock_w3):
    # Setup
    mock_w3.return_value.is_connected.return_value = True

    # Execute
    client = W3Client(mock_provider)
    client.connect()

    # Assert
    assert client.w3 is not None
    assert client.health.connection_failures == 0


def test_w3_client_connect_failure(mock_provider, mock_w3):
    # Setup
    mock_w3.return_value.is_connected.return_value = False

    # Execute
    client = W3Client(mock_provider)

    # Assert
    with pytest.raises(ConnectionError):
        client.connect()
    assert client.health.connection_failures == 1


def test_get_latest_block_number(mock_provider, mock_w3):
    # Setup
    mock_w3.return_value.is_connected.return_value = True
    mock_w3.return_value.eth.block_number = 12345

    # Execute
    client = W3Client(mock_provider)
    client.connect()
    block_number = client.get_latest_block_number()

    # Assert
    assert block_number == 12345
    assert client.health.block_failures == 0


def test_get_block_success(mock_provider, mock_w3):
    # Setup
    mock_w3.return_value.is_connected.return_value = True
    mock_block = {"number": 12345, "timestamp": 1678901234, "transactions": []}
    mock_w3.return_value.eth.get_block.return_value = mock_block

    # Execute
    client = W3Client(mock_provider)
    client.connect()
    block = client.get_block(12345)

    # Assert
    assert block == mock_block
    assert client.health.block_failures == 0


def test_validate_block_success(mock_provider, mock_w3):
    # Setup
    mock_w3.return_value.is_connected.return_value = True
    raw_block = {
        "number": 12345,
        "timestamp": 1678901234,
        "transactions": ["tx1", "tx2"],
    }

    # Execute
    client = W3Client(mock_provider)
    client.connect()
    block = client.validate_block(raw_block)

    # Assert
    assert block.number == raw_block["number"]
    assert block.timestamp == raw_block["timestamp"]
    assert block.tx_count == len(raw_block["transactions"])
    assert client.health.block_failures == 0
