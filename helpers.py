import os
from typing import List

import yaml
from dotenv import load_dotenv

import config
from models.provider import Provider

logging = config.setup_logging()
logger = logging.getLogger("helpers")


def load_providers(path: str) -> List[Provider]:
    """Load providers from YAML config and inject API keys from environment."""
    try:
        load_dotenv()

        with open(path) as f:
            yaml_config = yaml.safe_load(f)

        if (
            not yaml_config
            or "providers" not in yaml_config
            or len(yaml_config["providers"]) < 2
        ):
            raise ValueError("Config must contain at least two providers")

        providers = []
        for _id, data in yaml_config["providers"].items():
            logger.info(f"Loading provider: {data['name']}")

            if data.get("api_key", False):
                api_key = os.getenv(f"{data['name']}_API_KEY")
                if api_key:
                    data["url"] = f"{data['url']}/{api_key}"
                else:
                    logger.warning(f"Missing API key for {_id}")

            providers.append(Provider(**data))

        return providers

    except FileNotFoundError:
        logger.error(f"Config file not found: {path}")
        raise
    except yaml.YAMLError:
        logger.error(f"Invalid YAML in config: {path}")
        raise
    except Exception as e:
        logger.error(f"Failed to load providers: {str(e)}")
        raise
