# Block Streamer

A lightweight Ethereum block streamer that fetches blocks from the blockchain using multiple providers with automatic failover.

## Features

- **Multiple Provider Support**: Connect to multiple Ethereum RPC providers (Alchemy, Infura, etc.)
- **Hot-swappable Providers**: Automatically switch between providers if one fails
- **Resilient Processing**: Retry logic and error handling to ensure no blocks are missed
- **Lightweight Design**: Minimal code with separation of concerns

## Requirements

- Python 3.10+
- Web3.py
- PyYAML
- Pydantic

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/block-streamer.git
cd block-streamer

# Install dependencies
pip install -e .
```

## Configuration

Update the `providers.yml` file with your own provider URLs:

```yaml
providers:
  provider1:
    name: "Provider Name"
    url: "https://your-provider-url"
    type: "http"
```

Make sure to add at least two providers for failover functionality.

## Usage

```bash
# Start the block streamer
python main.py
```

## Project Structure

- `core/`: Core functionality
  - `streamer.py`: Block streaming logic
  - `hotswap.py`: Provider switching mechanism
  - `w3_client.py`: Web3 client wrapper
- `models/`: Data models
  - `provider.py`: Provider configuration model
  - `block.py`: Block data model
- `config.py`: Configuration settings
- `helpers.py`: Utility functions
- `providers.yml`: Provider configuration file

## Customization

You can adjust the following parameters in `config.py`:
- `POLL_INTERVAL`: Time between block checks
- `PROVIDER_TIMEOUT`: Provider request timeout
- `PROVIDER_MAX_RETRIES`: Number of retry attempts
- `HEALTH_CHECK_INTERVAL`: Interval for provider health checks
