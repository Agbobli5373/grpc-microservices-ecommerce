from pydantic import BaseModel
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: str

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    product_id: str
    quantity: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: str
    total_price: float

    class Config:
        from_attributes = True


class ProductList(BaseModel):
    products: List[Product]


class OrderList(BaseModel):
    orders: List[Order]
