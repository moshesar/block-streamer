import logging

from dotenv import load_dotenv

import config
from core.hotswap import HotswapManager
from core.streamer import BlockStreamer
from helpers import load_providers

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL), format=config.LOG_FORMAT)
logger = logging.getLogger("main")

load_dotenv()


if __name__ == "__main__":
    # Load all providers from the config file
    providers = load_providers(path=config.PROVIDERS_CONFIG_FILE)

    # Create the hotswap manager with all available providers
    manager = HotswapManager(providers)

    # Create the block streamer
    streamer = BlockStreamer(hotswap_manager=manager)

    # Start streaming blocks
    streamer.stream()
