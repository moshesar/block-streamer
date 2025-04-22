# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry==1.7.1

# Copy project files
COPY pyproject.toml poetry.lock README.md ./
COPY core/ ./core/
COPY models/ ./models/
COPY *.py ./
COPY providers.yml ./

# Configure Poetry to not create virtual environment in container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Run the service
CMD ["poetry", "run", "python", "main.py"] 