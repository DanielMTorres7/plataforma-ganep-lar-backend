# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install locales and generate pt_BR.UTF-8
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev locales && \
    sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    rm -rf /var/lib/apt/lists/*
ENV LANG=pt_BR.UTF-8
ENV LC_ALL=pt_BR.UTF-8

# Copy the pyproject.toml and poetry.lock (if available) to the container
COPY pyproject.toml ./
COPY uv.lock ./

# Install uv (dependency manager)
RUN pip install --no-cache-dir uv

# Install dependencies
RUN uv sync
# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["uv", "run", "ganep_lar/main.py"]
