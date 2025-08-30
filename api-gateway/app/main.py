from fastapi import FastAPI, HTTPException
from typing import List
import logging

from .models import Product, Order, ProductCreate, OrderCreate, ProductList, OrderList
from .clients import ProductServiceClient, OrderServiceClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ecommerce Microservices API Gateway",
    description="REST API gateway for product and order microservices",
    version="1.0.0"
)


@app.get("/products", response_model=ProductList)
async def list_products():
    """List all products"""
    try:
        async with ProductServiceClient() as client:
            products = await client.list_products()
            return ProductList(products=products)
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/products", response_model=Product)
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        async with ProductServiceClient() as client:
            created_product = await client.create_product(product)
            return created_product
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    try:
        async with ProductServiceClient() as client:
            product = await client.get_product(product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/orders", response_model=OrderList)
async def list_orders():
    """List all orders"""
    try:
        async with OrderServiceClient() as client:
            orders = await client.list_orders()
            return OrderList(orders=orders)
    except Exception as e:
        logger.error(f"Error listing orders: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/orders", response_model=Order)
async def create_order(order: OrderCreate):
    """Create a new order"""
    try:
        async with OrderServiceClient() as client:
            created_order = await client.create_order(order)
            return created_order
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get a specific order by ID"""
    try:
        async with OrderServiceClient() as client:
            order = await client.get_order(order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order {order_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api-gateway"}
