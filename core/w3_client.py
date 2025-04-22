import logging

from web3 import Web3

import config
from core.health import ProviderHealth, measure_time
from models.block import Block
from models.provider import Provider

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL), format=config.LOG_FORMAT)
logger = logging.getLogger("w3_client")


class W3Client:
    def __init__(self, provider: Provider):
        self.provider = provider
        self.w3 = None
        self.health = ProviderHealth(provider.name)

    @measure_time
    def connect(self):
        """Connect to the provider."""
        try:
            # Set up the Web3 connection
            self.w3 = Web3(
                Web3.HTTPProvider(
                    self.provider.url,
                    request_kwargs={"timeout": config.PROVIDER_TIMEOUT},
                )
            )

            # Check if the connection is successful
            if not self.w3.is_connected():
                raise ConnectionError(
                    f"Failed to connect to provider: {self.provider.name}"
                )

            logger.info(f"Connected to provider: {self.provider.name}")

        except Exception as e:
            logger.error(f"Connection error for {self.provider.name}: {str(e)}")
            self.health.connection_failures += 1
            raise

    @measure_time
    def get_latest_block_number(self):
        """Get the latest block number."""
        try:
            return self.w3.eth.block_number
        except Exception as e:
            self.health.block_failures += 1
            logger.error(
                f"Error getting latest block from {self.provider.name}: {str(e)}"
            )
            raise

    @measure_time
    def get_block(self, block_number: int):
        """Get block data"""
        try:
            block_data = self.w3.eth.get_block(block_number, full_transactions=False)
            return block_data

        except Exception as e:
            self.health.block_failures += 1
            logger.error(
                f"Error getting Block #{block_number} from {self.provider.name}: {str(e)}"
            )
            raise

    def validate_block(self, block: dict) -> Block:
        try:
            block = Block.from_raw(block)
            logger.info(f"Validated | #{block.number}")

            return block

        except Exception as e:
            self.health.block_failures += 1
            logger.error(f"Error validating #{block}: {str(e)}")
            raise

    def process_block(self, block: Block):
        """For now just log it"""
        try:
            logger.info(
                f"Processed | #{block.number} | ts: {block.timestamp} | txs: {block.tx_count}"
            )
        except Exception as e:
            logger.error(f"Error processing block #{block}: {str(e)}")
            self.health.block_failures += 1
