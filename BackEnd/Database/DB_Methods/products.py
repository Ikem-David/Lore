from sqlalchemy.orm import Session
from Database.tables import Products
from Schema import products


def get_all_products(db: Session):
	return db.query(Products).all()


def get_product(db: Session, product_id: int):
	return db.query(Products).filter(Products.id == product_id).first()


def get_product_by_name(db: Session, name: str):
	return db.query(Products).filter(Products.name == name).first()


def create_product(db: Session, req: products.CreateProduct,image_url:str):
	new_data = Products(
		name=req.name,
		price=req.price,
		categorie=req.categorie,
		image_url=image_url,
		stock=req.stock
	)

	db.add(new_data)
	db.commit()
	db.refresh(new_data)
	return new_data


def update_product(db: Session, product_id: int, req: products.UpdateProduct,image_url:str):
	product = db.query(Products).filter(Products.id == product_id).first()

	if not product:
		return None

	if req.name is not None:
		product.name = req.name

	if req.price is not None:
		product.price = req.price

	if req.categorie is not None:
		product.categorie = req.categorie

	if image_url is not None:
		product.image_url = image_url

	if req.stock is not None:
		product.stock = req.stock

	db.commit()
	db.refresh(product)
	return product


def delete_product(db: Session, product_id: int):
	product = db.query(Products).filter(Products.id == product_id).first()

	if not product:
		return None

	db.delete(product)
	db.commit()
	return product
