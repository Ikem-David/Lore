from pydantic import BaseModel
from typing import Optional
class ProductBase(BaseModel):
    name : str
    price : float
    categorie : str
    stock : int
class CreateProduct(ProductBase):
    pass

class UpdateProduct(BaseModel):
    name : Optional[str] = None
    price : Optional[float] = None
    categorie : Optional[str] = None
    stock : Optional[int] = None

class DeleteProduct(BaseModel):
    id : int

class ProductResponse(ProductBase):
    id : int
    image_url : str
    class Config:
        from_attributes = True