
# Ecommerce Microservices POC — Product + Order + API Gateway

Overview
- product-service: gRPC server that owns Product resources and its DB (SQLite for POC). List/Get/Create products.
- order-service: gRPC server that owns Order resources and its DB (SQLite for POC). When creating an order it validates the product by calling product-service (gRPC) and computes total price = product.price * quantity.
- api-gateway: FastAPI REST API that translates external REST requests to internal gRPC calls to the services.
- Each service generates its gRPC Python stubs at build time from protos.

This is a minimal, runnable microservice proof-of-concept where each service "owns" its resources.

Quick start (requires Docker + docker-compose)
1. Build & run:
   docker-compose up --build

2. REST endpoints (api-gateway)
   - List products
     curl http://127.0.0.1:8000/products

   - Create product
     curl -X POST http://127.0.0.1:8000/products \
       -H "Content-Type: application/json" \
       -d '{"name":"T-Shirt","description":"100% cotton","price":19.99}'

   - Get product
     curl http://127.0.0.1:8000/products/<id>

   - List orders
     curl http://127.0.0.1:8000/orders

   - Create order (use a real product id)
     curl -X POST http://127.0.0.1:8000/orders \
       -H "Content-Type: application/json" \
       -d '{"product_id":"<product-id>","quantity":2}'

   - Get order
     curl http://127.0.0.1:8000/orders/<id>

Notes
- product-service listens on 50051 inside container.
- order-service listens on 50052 inside container and calls product-service to validate products.
- api-gateway listens on 8000 and calls both services.
- For simplicity each service contains a copy of the proto files and generates its own proto_gen at build time. For production you would publish versioned proto artifacts or share proto_gen as a package.
- Replace SQLite with Postgres and add migrations for production workloads.
