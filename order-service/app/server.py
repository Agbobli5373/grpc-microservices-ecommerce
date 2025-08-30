import asyncio
import logging
import grpc
from concurrent import futures

from proto_gen.order_pb2_grpc import add_OrderServiceServicer_to_server
from .servicer import OrderServicer
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
    add_OrderServiceServicer_to_server(OrderServicer(), server)

    # Add insecure port
    server.add_insecure_port('[::]:50052')
    logger.info("Order service listening on port 50052")

    # Start server
    await server.start()
    logger.info("Order service started")

    # Wait for termination
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down order service")
        await server.stop(0)


if __name__ == '__main__':
    asyncio.run(serve())
