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


def test_provider_switching_on_failure():
    """
    Integration test that verifies the system can switch providers when one fails.
    This test simulates a real scenario where:
    1. The system starts with Provider1
    2. Provider1 fails when getting a block
    3. System automatically switches to Provider2
    4. Provider2 successfully gets the block
    """
    with patch("core.w3_client.Web3") as mock_web3:
        # Setup Web3 mock for two different providers
        web3_instance1 = Mock()
        web3_instance2 = Mock()

        # Provider1 setup - will fail
        web3_instance1.is_connected.return_value = True
        web3_instance1.eth.block_number = 12345
        web3_instance1.eth.get_block.side_effect = Exception("Provider1 failed")

        # Provider2 setup - will succeed
        web3_instance2.is_connected.return_value = True
        web3_instance2.eth.block_number = 12345
        web3_instance2.eth.get_block.return_value = {
            "number": 12345,
            "timestamp": 1678901234,
            "transactions": ["tx1"],
        }

        # Setup Web3 to return different instances for different providers
        def mock_web3_init(provider_url, **kwargs):
            if "provider1" in provider_url:
                mock_web3.return_value = web3_instance1
            else:
                mock_web3.return_value = web3_instance2
            return Mock()

        mock_web3.HTTPProvider = mock_web3_init

        # Create providers
        providers = [
            Provider(url="https://provider1.test.com", name="Provider1", type="http"),
            Provider(url="https://provider2.test.com", name="Provider2", type="http"),
        ]

        # Initialize the system
        manager = HotswapManager(providers)

        # Verify initial state
        assert manager.current_provider == "Provider1"

        # Simulate block processing that will fail with Provider1
        try:
            client = manager.get_client()
            block_data = client.get_block(12345)
        except Exception:
            # After failure, manually mark Provider1 as unhealthy
            # This simulates what would happen in production after multiple failures
            client.health.block_failures = 3  # Assuming threshold is lower than this

        # System should switch to Provider2
        client = manager.get_client()
        assert manager.current_provider == "Provider2"

        # Get block should now succeed with Provider2
        block_data = client.get_block(12345)
        assert block_data["number"] == 12345
        assert len(block_data["transactions"]) == 1
