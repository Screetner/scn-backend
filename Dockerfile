# Build stage
FROM python:3.9-slim as build

WORKDIR /app

# Cache Python packages
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Production stage
FROM python:3.9-slim

WORKDIR /app

# Copy Python packages from the build stage
COPY --from=build /install /usr/local

# Copy the application code
COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]