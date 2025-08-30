import uuid
from typing import List
import logging
import grpc

from google.protobuf import empty_pb2
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from proto_gen.order_pb2 import Order as ProtoOrder, ListOrdersResponse
from proto_gen.order_pb2_grpc import OrderServiceServicer
from .models import Order, OrderCreate
from .database import get_session
from .client import ProductServiceClient

logger = logging.getLogger(__name__)


class OrderServicer(OrderServiceServicer):
    async def ListOrders(self, request, context):
        """List all orders"""
        try:
            async for session in get_session():
                result = await session.execute(select(Order))
                orders = result.scalars().all()

                proto_orders = []
                for order in orders:
                    proto_order = ProtoOrder(
                        id=order.id,
                        product_id=order.product_id,
                        quantity=order.quantity,
                        total_price=order.total_price
                    )
                    proto_orders.append(proto_order)

                return ListOrdersResponse(orders=proto_orders)

        except Exception as e:
            logger.error(f"Error listing orders: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return ListOrdersResponse()

    async def GetOrder(self, request, context):
        """Get a specific order by ID"""
        try:
            async for session in get_session():
                result = await session.execute(
                    select(Order).where(Order.id == request.id)
                )
                order = result.scalar_one_or_none()

                if not order:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Order not found")
                    return ProtoOrder()

                return ProtoOrder(
                    id=order.id,
                    product_id=order.product_id,
                    quantity=order.quantity,
                    total_price=order.total_price
                )

        except Exception as e:
            logger.error(f"Error getting order {request.id}: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return ProtoOrder()

    async def CreateOrder(self, request, context):
        """Create a new order - validates product exists and calculates total price"""
        try:
            # Validate input
            if not request.product_id or request.quantity <= 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid order data")
                return ProtoOrder()

            # Validate product exists by calling product-service
            async with ProductServiceClient() as client:
                product = await client.get_product(request.product_id)

                if not product:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Product not found")
                    return ProtoOrder()

                # Calculate total price
                total_price = product["price"] * request.quantity

                order_data = OrderCreate(
                    product_id=request.product_id,
                    quantity=request.quantity
                )

                async for session in get_session():
                    order = Order(
                        **order_data.model_dump(),
                        total_price=total_price
                    )
                    session.add(order)
                    await session.commit()
                    await session.refresh(order)

                    return ProtoOrder(
                        id=order.id,
                        product_id=order.product_id,
                        quantity=order.quantity,
                        total_price=order.total_price
                    )

        except grpc.RpcError as e:
            logger.error(f"gRPC error creating order: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Product service unavailable")
            return ProtoOrder()
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return ProtoOrder()
