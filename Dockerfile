# Use a modern Python base image
FROM python:3.13-slim-bookworm

# Install UV for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies (without the current package)
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy the rest of the application
COPY . .

# Install the project in editable mode if necessary, or just install it
RUN uv pip install --system --no-cache -e .

# Expose port (adjust if your main.py uses a specific one)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]
