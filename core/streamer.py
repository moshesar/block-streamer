import logging
import time

import config
from core.hotswap import HotswapManager
from core.w3_client import W3Client

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL), format=config.LOG_FORMAT)
logger = logging.getLogger("streamer")


class BlockStreamer:
    def __init__(self, hotswap_manager: HotswapManager):
        self.manager = hotswap_manager
        self.last_block = None

    def stream(self):
        """Stream blocks from the blockchain."""
        logger.info("Streaming...")
        while True:
            try:
                client: W3Client = self.manager.get_client()

                current_block = client.get_latest_block_number()
                if self.last_block is None:
                    self.last_block = current_block - 1
                    logger.info(
                        f"{client.provider.name} Initialized at Block #{self.last_block}"
                    )

                if current_block > self.last_block:
                    logger.info(
                        f"Found {current_block - self.last_block} new blocks. Processing..."
                    )

                    for block_number in range(self.last_block + 1, current_block + 1):
                        block_data = client.get_block(block_number)
                        block = client.validate_block(block_data)
                        client.process_block(block)
                        self.last_block = block_number

                time.sleep(config.POLL_INTERVAL)
            except Exception:
                time.sleep(config.POLL_INTERVAL)
