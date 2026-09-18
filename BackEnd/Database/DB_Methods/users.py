from sqlalchemy.orm import Session
from Database.tables import Users, CartItem, Products
from Schema import users, cartitems
from components import hasher

# User Account Operations
def get_all_users(db:Session):
    return db.query(Users).all()

def get_user(db:Session,req:str):
    return db.query(Users).filter(Users.username == req).first()

def get_user_email(db:Session,req:str):
    return db.query(Users).filter(Users.email == req).first()

def create_user(db:Session,req:users.CreateUser):
    new_data = Users(
        username = req.username,
        email = req.email,
        password = hasher.Hash.hash_password(req.password)
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

def update_user(db: Session, user_id:int, req: users.UpdateUser):
    user = db.query(Users).filter(
        Users.id == user_id
    ).first()

    if not user:
        return None

    if req.username is not None:
        user.username = req.username

    if req.email is not None:
        user.email = req.email

    if req.password is not None:
        user.password = hasher.Hash.hash_password(req.password)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db:Session,user_id:int):
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        return None

    db.delete(user)
    db.commit()
    return user

# User's Cart Operations
def create_cart_item(db: Session, req: cartitems.CreateCartItem):
    new_item = CartItem(
        user_id=req.user_id,
        product_id=req.product_id,
        quantity=req.quantity
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def get_cart_item(db: Session, item_id: int):
    return db.query(CartItem).filter(
        CartItem.id == item_id
    ).first()


def get_user_cart(db: Session, user_id: int):
    return db.query(CartItem).filter(
        CartItem.user_id == user_id
    ).all()


def add_user_cart_item(db: Session, user_id: int, req: cartitems.CreateCurrentCartItem):
    product = db.query(Products).filter(Products.id == req.product_id).first()
    if product is None:
        raise ValueError("Product not found")

    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == req.product_id
    ).first()

    next_quantity = req.quantity + (existing_item.quantity if existing_item else 0)
    if next_quantity > product.stock:
        raise ValueError(f"Only {product.stock} item(s) available")

    if existing_item:
        existing_item.quantity += req.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    return create_cart_item(
        db,
        cartitems.CreateCartItem(
            user_id=user_id,
            product_id=req.product_id,
            quantity=req.quantity
        )
    )


def update_user_cart_item(
    db: Session,
    user_id: int,
    product_id: int,
    req: cartitems.UpdateCartItem
):
    item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if not item:
        return None

    if req.quantity is not None:
        product = db.query(Products).filter(Products.id == product_id).first()
        if product is None:
            return None
        if req.quantity > product.stock:
            raise ValueError(f"Only {product.stock} item(s) available")
        item.quantity = req.quantity

    db.commit()
    db.refresh(item)
    return item


def delete_user_cart_item(db: Session, user_id: int, product_id: int):
    item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if not item:
        return None

    db.delete(item)
    db.commit()
    return item


def update_cart_item(
    db: Session,
    item_id: int,
    req: cartitems.UpdateCartItem
):
    item = db.query(CartItem).filter(
        CartItem.id == item_id
    ).first()

    if not item:
        return None

    if req.quantity is not None:
        item.quantity = req.quantity

    db.commit()
    db.refresh(item)

    return item

def delete_cart_item(db: Session, item_id: int):
    item = db.query(CartItem).filter(
        CartItem.id == item_id
    ).first()

    if not item:
        return None

    db.delete(item)
    db.commit()

    return item