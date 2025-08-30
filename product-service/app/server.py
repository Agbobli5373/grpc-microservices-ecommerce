import asyncio
import logging
import grpc
from concurrent import futures

from proto_gen.product_pb2_grpc import add_ProductServiceServicer_to_server
from .servicer import ProductServicer
from .database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def serve():
    """Start the gRPC server"""
    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Create gRPC server
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add servicer
    add_ProductServiceServicer_to_server(ProductServicer(), server)

    # Add insecure port
    server.add_insecure_port('[::]:50051')
    logger.info("Product service listening on port 50051")

    # Start server
    await server.start()
    logger.info("Product service started")

    # Wait for termination
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down product service")
        await server.stop(0)


if __name__ == '__main__':
    asyncio.run(serve())
