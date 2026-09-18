from sqlalchemy.orm import Session
from Database.tables import CartItem, Products, Purchases, PurchaseItem
from Schema import purchases, purchaseitems

# Purchase Operations
def get_all_purchases(db: Session):
	return db.query(Purchases).all()


def get_purchase(db: Session, purchase_id: int):
	return db.query(Purchases).filter(Purchases.id == purchase_id).first()


def get_user_purchases(db: Session, user_id: int):
	return db.query(Purchases).filter(Purchases.user_id == user_id).all()


def create_purchase(db: Session, user_id: int, req: purchases.PurchasesBase):
	new_data = Purchases(
		user_id=user_id,
		total_price=req.total_price
	)

	db.add(new_data)
	db.commit()
	db.refresh(new_data)
	return new_data


def checkout(db: Session, user_id: int):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        return None

    total_price = 0
    products_by_id = {}
    for cart_item in cart_items:
        product = db.query(Products).filter(Products.id == cart_item.product_id).first()
        if product is None:
            raise ValueError("A product in your cart no longer exists")
        if cart_item.quantity > product.stock:
            raise ValueError(f"Only {product.stock} {product.name} item(s) available")
        products_by_id[product.id] = product
        total_price += product.price * cart_item.quantity

    purchase = Purchases(user_id=user_id, total_price=total_price)
    db.add(purchase)
    db.flush()

    for cart_item in cart_items:
        product = products_by_id[cart_item.product_id]
        db.add(PurchaseItem(
            purchase_id=purchase.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            price=product.price
        ))
        product.stock -= cart_item.quantity
        db.delete(cart_item)

    db.commit()
    db.refresh(purchase)
    return purchase


def update_purchase(
	db: Session,
	purchase_id: int,
	req: purchases.PurchasesBase
):
	purchase = db.query(Purchases).filter(Purchases.id == purchase_id).first()

	if not purchase:
		return None

	purchase.total_price = req.total_price

	db.commit()
	db.refresh(purchase)
	return purchase


def delete_purchase(db: Session, purchase_id: int):
	purchase = db.query(Purchases).filter(Purchases.id == purchase_id).first()

	if not purchase:
		return None

	db.delete(purchase)
	db.commit()
	return purchase

# Puchased Item's Operations
def create_purchase_item(
    db: Session,
    req: purchaseitems.CreatePurchaseItem
):
    new_item = PurchaseItem(
        purchase_id=req.purchase_id,
        product_id=req.product_id,
        quantity=req.quantity,
        price=req.price
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def get_purchase_item(db: Session, item_id: int):
    return db.query(PurchaseItem).filter(
        PurchaseItem.id == item_id
    ).first()


def get_purchaseitems(db: Session, purchase_id: int):
    return db.query(PurchaseItem).filter(
        PurchaseItem.purchase_id == purchase_id
    ).all()


def update_purchase_item(
    db: Session,
    item_id: int,
    req: purchaseitems.UpdatePurchaseItem
):
    item = db.query(PurchaseItem).filter(
        PurchaseItem.id == item_id
    ).first()

    if not item:
        return None

    if req.quantity is not None:
        item.quantity = req.quantity

    if req.price is not None:
        item.price = req.price

    db.commit()
    db.refresh(item)

    return item


def delete_purchase_item(db: Session, item_id: int):
    item = db.query(PurchaseItem).filter(
        PurchaseItem.id == item_id
    ).first()

    if not item:
        return None

    db.delete(item)
    db.commit()

    return item