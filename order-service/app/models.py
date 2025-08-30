from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class Order(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    product_id: str = Field(index=True)
    quantity: int = Field(gt=0)
    total_price: float = Field(gt=0)

    class Config:
        arbitrary_types_allowed = True


class OrderCreate(SQLModel):
    product_id: str
    quantity: int


class OrderUpdate(SQLModel):
    product_id: Optional[str] = None
    quantity: Optional[int] = None
    total_price: Optional[float] = None
