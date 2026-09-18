from pydantic import BaseModel, Field
from typing import Optional
class CartResponse(BaseModel):
    id: int
    user_id : int
    product_id : int
    quantity : int
    class Config:
        from_attributes = True
class CreateCartItem(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(default=1, gt=0)

class CreateCurrentCartItem(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)

class UpdateCartItem(BaseModel):
    quantity: Optional[int] = Field(default=None, gt=0)