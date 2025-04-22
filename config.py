import logging

# Time in seconds before an unhealthy provider becomes eligible for recovery
PROVIDER_TIMEOUT = 30

# Minimum seconds between health checks for a single provider
HEALTH_CHECK_MIN_INTERVAL = 5

# Number of response times to keep for average calculation
RESPONSE_TIME_WINDOW = 5

# Number of network failures before marked unhealthy
NETWORK_FAILURE_THRESHOLD = 2

# Number of connection failures before marked unhealthy
CONNECTION_FAILURE_THRESHOLD = 2

# Number of block failures before marked unhealthy
BLOCK_FAILURE_THRESHOLD = 2

# Time in seconds before an unhealthy provider becomes eligible for recovery
PROVIDER_RECOVERY_TIME = 30


# Streamer settings
POLL_INTERVAL = 2

# Logging
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
LOG_LEVEL = "INFO"

# Provider types
PROVIDER_TYPES = ["http", "websocket"]

# Default provider configuration file
PROVIDERS_CONFIG_FILE = "providers.yml"


def setup_logging():
    """Centralized logging configuration to be used across modules."""
    logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
    return logging
