import grpc
import logging
from typing import Optional

from proto_gen.product_pb2 import GetProductRequest
from proto_gen.product_pb2_grpc import ProductServiceStub

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

    async def get_product(self, product_id: str) -> Optional[dict]:
        """Get product details from product service"""
        try:
            request = GetProductRequest(id=product_id)
            response = await self.stub.GetProduct(request)

            if response.id:  # Product exists
                return {
                    "id": response.id,
                    "name": response.name,
                    "description": response.description,
                    "price": response.price
                }
            else:
                return None

        except grpc.RpcError as e:
            logger.error(f"gRPC error getting product {product_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            return None
