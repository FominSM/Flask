from pydantic import BaseModel, Field
from datetime import date


class UserIn(BaseModel):
    name: str = Field(..., min_length=2)
    surname: str = Field(..., min_length=2)
    birthday: str = Field(..., )
    adress: str = Field(..., )
    email: str = Field(..., max_length=128)
    password: str = Field(..., min_length=6)


class User(BaseModel):
    id: int
    name: str = Field(..., max_length=32)
    email: str = Field(..., max_length=128)


class ProductIn(BaseModel):
    title: str = Field(..., min_length=2)
    description: str = Field(..., min_length=2)
    price: float = Field(...)


class Product(BaseModel):
    id: int
    title: str = Field(..., min_length=2)
    description: str = Field(..., min_length=2)
    price: float = Field(...)


class OrderIn(BaseModel):
    date_order: str = Field(...,)
    status_order: str = Field(..., max_length=100)
    id_user: int = Field(...)
    id_product: int = Field(...)


class Order(BaseModel):
    id: int
    id_user: int = Field(...)
    id_product: int = Field(...)
    date_order: str = Field(...,)
    status_order: str = Field(..., max_length=100)