import os
from typing import List

import yaml

import config
from models.provider import Provider

# Get centralized logger
logging = config.setup_logging()
logger = logging.getLogger("helpers")


def load_providers(path: str) -> List[Provider]:
    """Load all providers from the YAML configuration file."""
    logger.info(f"Loading providers from {path}")

    with open(path, "r") as f:
        yaml_config = yaml.safe_load(f)

    if not yaml_config or "providers" not in yaml_config:
        raise ValueError("Invalid or empty providers configuration")

    if len(yaml_config["providers"].items()) < 2:
        raise ValueError("At least two providers must be provided.")

    providers = []

    for provider_id, provider_data in yaml_config["providers"].items():
        # Add the provider ID as the name if not specified
        if "name" not in provider_data:
            provider_data["name"] = provider_id

        # Handle API key if needed
        if provider_data.get("api_key") is True:
            env_key = f"{provider_id.upper()}_API_KEY"
            api_key = os.getenv(env_key)
            if not api_key:
                logger.warning(
                    f"No API key found in .env for {provider_id} (expected {env_key})"
                )
            else:
                # Remove any trailing slashes from URL and spaces
                provider_data["url"] = provider_data["url"].rstrip("/ ")
                if "?" in provider_data["url"]:
                    provider_data["url"] = f"{provider_data['url']}&apikey={api_key}"
                else:
                    provider_data["url"] = f"{provider_data['url']}/{api_key}"

        # Remove the api_key flag from the data before creating Provider
        provider_data.pop("api_key", None)

        provider = Provider(**provider_data)
        providers.append(provider)
        logger.info(f"Loaded provider: {provider.name}")

    logger.info(f"Loaded {len(providers)} providers from configuration")
    return providers
