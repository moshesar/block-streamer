# Block Streamer

<img src="Logo.png" alt="StockLight Logo" width="200"/>

A lightweight Ethereum block streamer that fetches blocks from the blockchain using multiple providers with automatic failover.
Serves as a simplified monolithic example to demonstrate the core concepts.
## Features

- **Multiple Provider Support**: Connect to multiple Ethereum RPC providers (Alchemy, Infura, etc.)
- **Hot-swappable Providers**: Automatically switch between providers if one fails
- **Resilient Processing**: Retry logic and error handling to ensure no blocks are missed
- **Lightweight Design**: Minimal code with separation of concerns
- **Containerized**: Easy deployment with Docker

## Quick Start with Docker

The easiest way to run the service is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/yourusername/block-streamer.git
cd block-streamer

# Create and edit the environment file for sensitive data
touch .env

# Add your API keys to .env:
ALCHEMY_API_KEY=your_alchemy_key
INFURA_API_KEY=your_infura_key

# Build the Docker images
docker-compose build

# Start the service (with logs)
docker-compose up block-streamer

# Or start in detached mode (background)
docker-compose up -d block-streamer

# View logs when running in detached mode
docker-compose logs -f block-streamer

# Stop the service
docker-compose down
```

## Running Tests with Docker

```bash
# Run all tests
docker-compose run tests

# Run specific test file
docker-compose run tests poetry run pytest tests/unit/test_models.py

# Run with coverage
docker-compose run tests poetry run pytest --cov=.
```

## Local Development Setup

### Prerequisites

- Python 3.10+
- Docker and Docker Compose (for containerized deployment)


### Installing Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to your PATH (if not automatically added)
# For macOS/Linux, add to your ~/.bashrc or ~/.zshrc:
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
poetry --version
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/block-streamer.git
cd block-streamer

# Install dependencies
poetry install

# Get the path to the virtual environment
poetry env info --path

# Activate virtual environment (use the path from previous command)
source $(poetry env info --path)/bin/activate

# Run the service
python main.py
```

### Running Tests Locally

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/unit/test_models.py

# Run with coverage
poetry run pytest --cov=.
```

## Configuration

### Provider Configuration

The service supports multiple Ethereum RPC providers for redundancy. Configure your providers in `providers.yml`:

```yaml
providers:
  chainstack:
    name: "CHAINSTACK"
    url: "https://your-chainstack-url"
    api_key: false
    type: "http"

  alchemy:
    name: "ALCHEMY"
    url: "https://eth-mainnet.g.alchemy.com/v2/${ALCHEMY_API_KEY}"
    api_key: true
    type: "http"

  infura:
    name: "INFURA"
    url: "https://mainnet.infura.io/v3/${INFURA_API_KEY}"
    api_key: true
    type: "http"
```

### Environment Variables

The project uses two types of configuration:

1. **Sensitive Information** (in `.env`):
```env
# Provider API keys only
ALCHEMY_API_KEY=your_alchemy_key
INFURA_API_KEY=your_infura_key
```

2. **Service Configuration** (in `config.py`):
```python
# These settings are managed in the config.py file
LOG_LEVEL=INFO
PROVIDER_TIMEOUT=30
POLL_INTERVAL=2
```

Do not put non-sensitive configuration in `.env` - use the `config.py` file instead.

## Project Structure

- `core/`: Core functionality
  - `streamer.py`: Block streaming logic
  - `hotswap.py`: Provider switching mechanism
  - `w3_client.py`: Web3 client wrapper
- `models/`: Data models
  - `provider.py`: Provider configuration model
  - `block.py`: Block data model
- `tests/`: Test suite
  - `unit/`: Unit tests
- `config.py`: Configuration settings
- `helpers.py`: Utility functions
- `providers.yml`: Provider configuration file

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
