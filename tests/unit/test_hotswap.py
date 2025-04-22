from unittest.mock import Mock, patch

import pytest

from core.hotswap import HotswapManager
from models.provider import Provider


@pytest.fixture
def mock_providers():
    return [
        Provider(url="https://provider1.test.com", name="Provider1", type="http"),
        Provider(url="https://provider2.test.com", name="Provider2", type="http"),
    ]


@pytest.fixture
def mock_w3_client():
    with patch("core.hotswap.W3Client") as mock:

        def create_instance(provider):
            client_instance = Mock()
            client_instance.health.is_healthy = True
            client_instance.connect.return_value = None
            client_instance.provider = provider
            return client_instance

        mock.side_effect = create_instance
        yield mock


def test_hotswap_manager_initialization(mock_providers, mock_w3_client):
    # Execute
    manager = HotswapManager(mock_providers)

    # Assert
    assert manager.providers == mock_providers
    assert len(manager.clients) == 2
    assert manager.current_provider == "Provider1"  # First provider should be selected
    assert mock_w3_client.call_count == 2


def test_hotswap_manager_get_client_healthy(mock_providers, mock_w3_client):
    # Setup
    manager = HotswapManager(mock_providers)

    # Execute
    client = manager.get_client()

    # Assert
    assert client.provider.name == "Provider1"
    assert manager.current_provider == "Provider1"


def test_hotswap_manager_swap_on_unhealthy(mock_providers, mock_w3_client):
    # Setup
    manager = HotswapManager(mock_providers)

    # Make first provider unhealthy
    manager.clients["Provider1"].health.is_healthy = False

    # Execute
    client = manager.get_client()

    # Assert
    assert manager.current_provider == "Provider2"
    assert client.provider.name == "Provider2"


def test_hotswap_manager_no_healthy_providers(mock_providers, mock_w3_client):
    # Setup
    manager = HotswapManager(mock_providers)

    # Make all providers unhealthy
    for client in manager.clients.values():
        client.health.is_healthy = False

    # Execute & Assert
    with pytest.raises(RuntimeError, match="No healthy providers available"):
        manager.get_client()


def test_hotswap_manager_initialization_failure(mock_providers, mock_w3_client):
    # Setup - all connect attempts will fail
    def fail_connect(provider):
        client = Mock()
        client.connect.side_effect = Exception("Connection failed")
        return client

    mock_w3_client.side_effect = fail_connect

    # Execute & Assert
    with pytest.raises(RuntimeError, match="No healthy providers available"):
        HotswapManager(mock_providers)
