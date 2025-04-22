import logging
from typing import List

import config
from core.w3_client import W3Client
from models.provider import Provider

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL), format=config.LOG_FORMAT)
logger = logging.getLogger("manager")


class HotswapManager:
    def __init__(self, providers: List[Provider]):
        self.providers = providers
        self.clients = {}
        self.current_provider = None

        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize all clients and select the first healthy one."""
        for provider in self.providers:
            try:
                client = W3Client(provider)
                client.connect()
                self.clients[provider.name] = client

                # Set the first working provider as current
                if not self.current_provider and client.health.is_healthy:
                    self.current_provider = provider.name
                    logger.info(f"Using {provider.name} as primary provider")
            except Exception as e:
                logger.warning(f"Failed to initialize {provider.name}: {e}")

        if not self.current_provider:
            raise RuntimeError("No healthy providers available")

    def get_client(self) -> W3Client:
        """Get a healthy client, switching providers if necessary."""
        if (
            not self.current_provider
            or not self.clients[self.current_provider].health.is_healthy
        ):
            self._swap()
        return self.clients[self.current_provider]

    def _swap(self):
        """Swap to the next healthy provider."""
        for name, client in self.clients.items():
            if client.health.is_healthy:
                self.current_provider = name
                logger.info(f"Swapped to: {name}")
                return

        raise RuntimeError("No healthy providers available")
