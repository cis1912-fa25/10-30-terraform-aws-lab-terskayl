FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ADD main.py .
ADD pyproject.toml .

# Install dependencies
RUN uv sync

# Expose port 80
EXPOSE 80

# Run the application
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "80"]
