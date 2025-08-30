import grpc
import logging
from typing import List, Optional

from proto_gen.product_pb2 import (
    GetProductRequest,
    CreateProductRequest,
    ListProductsResponse
)
from proto_gen.product_pb2_grpc import ProductServiceStub

from proto_gen.order_pb2 import (
    GetOrderRequest,
    CreateOrderRequest,
    ListOrdersResponse
)
from proto_gen.order_pb2_grpc import OrderServiceStub

from .models import Product, Order, ProductCreate, OrderCreate

logger = logging.getLogger(__name__)


class ProductServiceClient:
    def __init__(self, host: str = "product-service", port: int = 50051):
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.channel = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
        self.stub = ProductServiceStub(self.channel)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.channel:
            await self.channel.close()

    async def list_products(self) -> List[Product]:
        """List all products"""
        try:
            from google.protobuf import empty_pb2
            response: ListProductsResponse = await self.stub.ListProducts(empty_pb2.Empty())

            products = []
            for proto_product in response.products:
                product = Product(
                    id=proto_product.id,
                    name=proto_product.name,
                    description=proto_product.description,
                    price=proto_product.price
                )
                products.append(product)
            return products

        except grpc.RpcError as e:
            logger.error(f"gRPC error listing products: {e}")
            raise
        except Exception as e:
            logger.error(f"Error listing products: {e}")
            raise

    async def get_product(self, product_id: str) -> Optional[Product]:
        """Get a specific product"""
        try:
            request = GetProductRequest(id=product_id)
            response = await self.stub.GetProduct(request)

            if response.id:  # Product exists
                return Product(
                    id=response.id,
                    name=response.name,
                    description=response.description,
                    price=response.price
                )
            return None

        except grpc.RpcError as e:
            logger.error(f"gRPC error getting product {product_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            raise

    async def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product"""
        try:
            request = CreateProductRequest(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price
            )
            response = await self.stub.CreateProduct(request)

            return Product(
                id=response.id,
                name=response.name,
                description=response.description,
                price=response.price
            )

        except grpc.RpcError as e:
            logger.error(f"gRPC error creating product: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise


class OrderServiceClient:
    def __init__(self, host: str = "order-service", port: int = 50052):
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.channel = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
        self.stub = OrderServiceStub(self.channel)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.channel:
            await self.channel.close()

    async def list_orders(self) -> List[Order]:
        """List all orders"""
        try:
            from google.protobuf import empty_pb2
            response: ListOrdersResponse = await self.stub.ListOrders(empty_pb2.Empty())

            orders = []
            for proto_order in response.orders:
                order = Order(
                    id=proto_order.id,
                    product_id=proto_order.product_id,
                    quantity=proto_order.quantity,
                    total_price=proto_order.total_price
                )
                orders.append(order)
            return orders

        except grpc.RpcError as e:
            logger.error(f"gRPC error listing orders: {e}")
            raise
        except Exception as e:
            logger.error(f"Error listing orders: {e}")
            raise

    async def get_order(self, order_id: str) -> Optional[Order]:
        """Get a specific order"""
        try:
            request = GetOrderRequest(id=order_id)
            response = await self.stub.GetOrder(request)

            if response.id:  # Order exists
                return Order(
                    id=response.id,
                    product_id=response.product_id,
                    quantity=response.quantity,
                    total_price=response.total_price
                )
            return None

        except grpc.RpcError as e:
            logger.error(f"gRPC error getting order {order_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting order {order_id}: {e}")
            raise

    async def create_order(self, order_data: OrderCreate) -> Order:
        """Create a new order"""
        try:
            request = CreateOrderRequest(
                product_id=order_data.product_id,
                quantity=order_data.quantity
            )
            response = await self.stub.CreateOrder(request)

            return Order(
                id=response.id,
                product_id=response.product_id,
                quantity=response.quantity,
                total_price=response.total_price
            )

        except grpc.RpcError as e:
            logger.error(f"gRPC error creating order: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise
