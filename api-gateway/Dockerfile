# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto files and generate stubs
COPY protos/ ./protos/
RUN mkdir -p ./proto_gen
RUN python -m grpc_tools.protoc -I./protos --python_out=./proto_gen --grpc_python_out=./proto_gen ./protos/product.proto ./protos/order.proto

# Copy application code
COPY app/ ./app/

# Set Python path to include proto_gen
ENV PYTHONPATH=/app:/app/proto_gen

# Expose port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
