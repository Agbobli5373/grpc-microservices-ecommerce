import uuid
from typing import List
import logging
import grpc

from google.protobuf import empty_pb2
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from proto_gen.product_pb2 import Product as ProtoProduct, ListProductsResponse
from proto_gen.product_pb2_grpc import ProductServiceServicer
from .models import Product, ProductCreate
from .database import get_session

logger = logging.getLogger(__name__)


class ProductServicer(ProductServiceServicer):
    async def ListProducts(self, request, context):
        """List all products"""
        try:
            async for session in get_session():
                result = await session.execute(select(Product))
                products = result.scalars().all()

                proto_products = []
                for product in products:
                    proto_product = ProtoProduct(
                        id=product.id,
                        name=product.name,
                        description=product.description,
                        price=product.price
                    )
                    proto_products.append(proto_product)

                return ListProductsResponse(products=proto_products)

        except Exception as e:
            logger.error(f"Error listing products: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return ListProductsResponse()

    async def GetProduct(self, request, context):
        """Get a specific product by ID"""
        try:
            async for session in get_session():
                result = await session.execute(
                    select(Product).where(Product.id == request.id)
                )
                product = result.scalar_one_or_none()

                if not product:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Product not found")
                    return ProtoProduct()

                return ProtoProduct(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    price=product.price
                )

        except Exception as e:
            logger.error(f"Error getting product {request.id}: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return ProtoProduct()

    async def CreateProduct(self, request, context):
        """Create a new product"""
        try:
            # Validate input
            if not request.name or not request.description or request.price <= 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid product data")
                return ProtoProduct()

            product_data = ProductCreate(
                name=request.name,
                description=request.description,
                price=request.price
            )

            async for session in get_session():
                product = Product(**product_data.model_dump())
                session.add(product)
                await session.commit()
                await session.refresh(product)

                return ProtoProduct(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    price=product.price
                )

        except Exception as e:
            logger.error(f"Error creating product: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return ProtoProduct()
