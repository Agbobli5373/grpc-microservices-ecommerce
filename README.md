# Ecommerce Microservices POC

A complete proof-of-concept implementation of an ecommerce platform using microservices architecture with gRPC communication and REST API gateway.

## 🏗️ Architecture Overview

This project demonstrates a modern microservices architecture with three independent services:

### Services

- **product-service** (gRPC, Port 50051)

  - Manages product catalog with SQLite database
  - Provides CRUD operations for products
  - Async gRPC server with SQLModel ORM

- **order-service** (gRPC, Port 50052)

  - Manages customer orders with SQLite database
  - Validates products by calling product-service
  - Calculates total price automatically
  - Async gRPC server with cross-service communication

- **api-gateway** (REST, Port 8000)
  - FastAPI REST API gateway
  - Translates REST requests to gRPC calls
  - Provides external API access to the microservices

### Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │    │ Product Service │    │  Order Service  │
│    (FastAPI)    │◄──►│     (gRPC)      │◄──►│     (gRPC)      │
│                 │    │                 │    │                 │
│ • REST API      │    │ • Product CRUD  │    │ • Order CRUD    │
│ • Request       │    │ • SQLite DB     │    │ • SQLite DB     │
│   Translation   │    │ • Validation    │    │ • Price Calc    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────────┐
                    │  Docker Compose     │
                    │  • Service Network  │
                    │  • Volume Mounts    │
                    │  • Health Checks    │
                    └─────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Run the Application

1. **Clone and navigate to the repository**

   ```bash
   git clone https://github.com/Agbobli5373/grpc-microservices-ecommerce.git
   cd grpc-microservices-ecommerce
   ```

2. **Build and start all services**

   ```bash
   docker-compose up --build
   ```

3. **Verify services are running**
   ```bash
   docker-compose ps
   ```

The application will be available at:

- **API Gateway**: http://localhost:8000
- **Product Service**: localhost:50051 (gRPC)
- **Order Service**: localhost:50052 (gRPC)

## 📡 API Endpoints

### Products API

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | `/products`      | List all products    |
| POST   | `/products`      | Create a new product |
| GET    | `/products/{id}` | Get product by ID    |

**Create Product Example:**

```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "description": "High-quality wireless headphones with noise cancellation",
    "price": 199.99
  }'
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Wireless Headphones",
  "description": "High-quality wireless headphones with noise cancellation",
  "price": 199.99
}
```

### Orders API

| Method | Endpoint       | Description        |
| ------ | -------------- | ------------------ |
| GET    | `/orders`      | List all orders    |
| POST   | `/orders`      | Create a new order |
| GET    | `/orders/{id}` | Get order by ID    |

**Create Order Example:**

```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "550e8400-e29b-41d4-a716-446655440000",
    "quantity": 2
  }'
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "product_id": "550e8400-e29b-41d4-a716-446655440000",
  "quantity": 2,
  "total_price": 399.98
}
```

## 🛠️ Development Setup

### Local Development

1. **Install dependencies for each service:**

   ```bash
   # Product Service
   cd product-service
   pip install -r requirements.txt

   # Order Service
   cd ../order-service
   pip install -r requirements.txt

   # API Gateway
   cd ../api-gateway
   pip install -r requirements.txt
   ```

2. **Generate gRPC stubs:**

   ```bash
   # Product Service
   cd product-service
   python -m grpc_tools.protoc -I./protos --python_out=./proto_gen --grpc_python_out=./proto_gen ./protos/product.proto

   # Order Service (needs both protos)
   cd ../order-service
   python -m grpc_tools.protoc -I./protos --python_out=./proto_gen --grpc_python_out=./proto_gen ./protos/product.proto ./protos/order.proto

   # API Gateway (needs both protos)
   cd ../api-gateway
   python -m grpc_tools.protoc -I./protos --python_out=./proto_gen --grpc_python_out=./proto_gen ./protos/product.proto ./protos/order.proto
   ```

3. **Run services individually:**

   ```bash
   # Terminal 1: Product Service
   cd product-service
   python -m app.server

   # Terminal 2: Order Service
   cd order-service
   python -m app.server

   # Terminal 3: API Gateway
   cd api-gateway
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## 📁 Project Structure

```
ecommerce-microservices-poc/
├── product-service/              # Product management service
│   ├── app/
│   │   ├── models.py            # SQLModel product definitions
│   │   ├── database.py          # Database initialization
│   │   ├── servicer.py          # gRPC service implementation
│   │   └── server.py            # gRPC server startup
│   ├── protos/
│   │   └── product.proto        # Product service protobuf definition
│   ├── proto_gen/               # Generated gRPC stubs
│   ├── data/                    # SQLite database files
│   ├── Dockerfile               # Service containerization
│   └── requirements.txt         # Python dependencies
├── order-service/               # Order management service
│   ├── app/
│   │   ├── models.py            # SQLModel order definitions
│   │   ├── database.py          # Database initialization
│   │   ├── servicer.py          # gRPC service with product validation
│   │   ├── client.py            # Product service client
│   │   └── server.py            # gRPC server startup
│   ├── protos/
│   │   ├── product.proto        # Product service protobuf
│   │   └── order.proto          # Order service protobuf definition
│   ├── proto_gen/               # Generated gRPC stubs
│   ├── data/                    # SQLite database files
│   ├── Dockerfile               # Service containerization
│   └── requirements.txt         # Python dependencies
├── api-gateway/                 # REST API gateway
│   ├── app/
│   │   ├── models.py            # Pydantic REST models
│   │   ├── clients.py           # gRPC clients for both services
│   │   └── main.py              # FastAPI application
│   ├── protos/
│   │   ├── product.proto        # Product service protobuf
│   │   └── order.proto          # Order service protobuf
│   ├── proto_gen/               # Generated gRPC stubs
│   ├── Dockerfile               # Service containerization
│   └── requirements.txt         # Python dependencies
├── docker-compose.yml           # Multi-service orchestration
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
└── .github/
    └── copilot-instructions.md  # AI coding assistant guidelines
```

## 🧪 Testing

### End-to-End Testing

Test the complete flow:

1. **Create a product**
2. **List products**
3. **Create an order** (validates product exists)
4. **List orders**
5. **Test error handling** (invalid product ID)

### Example Test Script

```bash
#!/bin/bash

# Create product
PRODUCT_RESPONSE=$(curl -s -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","description":"Test Description","price":29.99}')

PRODUCT_ID=$(echo $PRODUCT_RESPONSE | jq -r '.id')
echo "Created product with ID: $PRODUCT_ID"

# Create order
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d "{\"product_id\":\"$PRODUCT_ID\",\"quantity\":3}"

# List orders
curl http://localhost:8000/orders
```

## 🛡️ Error Handling

The system includes comprehensive error handling:

- **Product Validation**: Orders validate product existence before creation
- **gRPC Error Propagation**: Errors are properly mapped from gRPC to REST
- **Database Constraints**: SQLModel enforces data integrity
- **Network Resilience**: Services handle gRPC connection failures

## 🔧 Technologies Used

### Core Technologies

- **Python 3.11**: Primary programming language
- **gRPC**: Inter-service communication
- **FastAPI**: REST API framework
- **SQLModel**: SQL database ORM
- **SQLite**: Database (POC - replace with PostgreSQL for production)

### Infrastructure

- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Protocol Buffers**: API definitions

### Development Tools

- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **Git**: Version control

## 🚀 Production Considerations

### Database

- Replace SQLite with PostgreSQL
- Add database migrations (Alembic)
- Implement connection pooling
- Add database monitoring

### Security

- Add authentication/authorization
- Implement TLS for gRPC communication
- Add API rate limiting
- Secure sensitive configuration

### Observability

- Add structured logging
- Implement health checks
- Add metrics collection
- Set up monitoring dashboards

### Scalability

- Add service discovery
- Implement load balancing
- Add caching layer (Redis)
- Consider Kubernetes deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built as a proof-of-concept for microservices architecture
- Demonstrates modern Python async patterns
- Showcases gRPC and REST API integration
- Provides foundation for production ecommerce systems

---

**Note**: This is a proof-of-concept implementation. For production use, consider the production considerations mentioned above.
