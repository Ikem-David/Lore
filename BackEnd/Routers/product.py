from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary.uploader
from Database.DB_Methods import products as product_methods
from Database.db import get_db
from auth import get_current_user
from typing import Optional
from Schema import products

router = APIRouter(
	prefix="/product",
	tags=['Product']
)


@router.get("/", response_model=list[products.ProductResponse])
def read_products(db: Session = Depends(get_db)):
	return product_methods.get_all_products(db)


@router.get("/name/{name}", response_model=products.ProductResponse)
def read_product_by_name(name: str, db: Session = Depends(get_db)):
	product = product_methods.get_product_by_name(db, name)
	if product is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
	return product


@router.get("/{product_id}", response_model=products.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
	product = product_methods.get_product(db, product_id)
	if product is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
	return product


@router.post("/", response_model=products.ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
		name : str = Form(...),
		price : int = Form(...),
		categorie : str = Form(...),
		stock : int = Form(...),
		image : UploadFile = File(...),
		db: Session = Depends(get_db),
		current_user = Depends(get_current_user)
	):

	if product_methods.get_product_by_name(db,name) is not None:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product name already exists")

	# Upload Image to Cloudinary
	result = cloudinary.uploader.upload(image.file)
	image_url = result["secure_url"]

	req = products.CreateProduct(
		name= name,
		price=price,
		categorie=categorie,
		stock=stock
	)

	return product_methods.create_product(db,req,image_url)


@router.put("/{product_id}", response_model=products.ProductResponse)
def update_product(
		product_id: int,
		name : Optional[str] = Form(None),
		price : Optional[int] = Form(None),
		categorie : Optional[str] = Form(None),
		stock : Optional[int] = Form(None),
		image : Optional[UploadFile] = File(None),
		db: Session = Depends(get_db),
		current_user = Depends(get_current_user)
	):

	req = products.UpdateProduct(
		name=name,
		price=price,
		categorie=categorie,
		stock=stock,
	)

	image_url = None

	if image is not None:
		result = cloudinary.uploader.upload(image.file)
		image_url = result["secure_url"]

	product = product_methods.update_product(db, product_id,req,image_url)
	if product is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
	return product


@router.delete("/{product_id}", response_model=products.ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
	product = product_methods.delete_product(db, product_id)
	if product is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
	return product