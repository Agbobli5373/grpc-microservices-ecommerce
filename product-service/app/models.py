from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class Product(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(index=True)
    description: str
    price: float = Field(gt=0)

    class Config:
        arbitrary_types_allowed = True


class ProductCreate(SQLModel):
    name: str
    description: str
    price: float


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
