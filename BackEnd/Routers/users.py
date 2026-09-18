from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Database.DB_Methods import users as user_methods
from Database.db import get_db
from auth import get_current_user
from Schema import cartitems, users

router = APIRouter(
	prefix="/users",
	tags=['Users'],
)

# User Endpoints
@router.get("/", response_model=list[users.UserResponse])
def read_users(db: Session = Depends(get_db)):
	return user_methods.get_all_users(db)


@router.get("/username/{username}", response_model=users.UserResponse)
def read_user(username: str, db: Session = Depends(get_db)):
	user = user_methods.get_user(db, username)
	if user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return user


@router.get("/email/{email}", response_model=users.UserResponse)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
	user = user_methods.get_user_email(db, email)
	if user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return user


@router.post("/", response_model=users.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(req: users.CreateUser, db: Session = Depends(get_db)):
	if user_methods.get_user(db, req.username) is not None:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

	if user_methods.get_user_email(db, req.email) is not None:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

	return user_methods.create_user(db, req)


@router.get("/me/cart", response_model=list[cartitems.CartResponse])
def read_current_user_cart(
	current_user=Depends(get_current_user),
	db: Session = Depends(get_db)
):
	return user_methods.get_user_cart(db, current_user.id)


@router.post("/me/cart", response_model=cartitems.CartResponse, status_code=status.HTTP_201_CREATED)
def create_current_user_cart_item(
	req: cartitems.CreateCurrentCartItem,
	current_user=Depends(get_current_user),
	db: Session = Depends(get_db)
):
	try:
		return user_methods.add_user_cart_item(db, current_user.id, req)
	except ValueError as error:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.put("/me/cart/{product_id}", response_model=cartitems.CartResponse)
def update_current_user_cart_item(
	product_id: int,
	req: cartitems.UpdateCartItem,
	current_user=Depends(get_current_user),
	db: Session = Depends(get_db)
):
	try:
		item = user_methods.update_user_cart_item(db, current_user.id, product_id, req)
	except ValueError as error:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
	if item is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
	return item


@router.delete("/me/cart/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user_cart_item(
	product_id: int,
	current_user=Depends(get_current_user),
	db: Session = Depends(get_db)
):
	item = user_methods.delete_user_cart_item(db, current_user.id, product_id)
	if item is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")


@router.put("/{user_id}", response_model=users.UserResponse)
def update_user(user_id: int, req: users.UpdateUser, db: Session = Depends(get_db)):
	user = user_methods.update_user(db, user_id, req)
	if user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return user


@router.delete("/{user_id}", response_model=users.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
	user = user_methods.delete_user(db, user_id)
	if user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return user

# Users Cart's Items Endpoints
@router.post("/cart/items", response_model=cartitems.CartResponse, status_code=status.HTTP_201_CREATED)
def create_cart_item(req: cartitems.CreateCartItem, db: Session = Depends(get_db)):
	user_cart = user_methods.get_user_cart(db, req.user_id)
	for item in user_cart:
		if item.product_id == req.product_id:
			return user_methods.update_cart_item(
				db,
				item.id,
				cartitems.UpdateCartItem(quantity=item.quantity + 1)
			)

	return user_methods.create_cart_item(db, req)


@router.get("/cart/items/{item_id}", response_model=cartitems.CartResponse)
def read_cart_item(item_id: int, db: Session = Depends(get_db)):
	item = user_methods.get_cart_item(db, item_id)
	if item is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
	return item


@router.get("/{user_id}/cart", response_model=list[cartitems.CartResponse])
def read_user_cart(user_id: int, db: Session = Depends(get_db)):
	return user_methods.get_user_cart(db, user_id)


@router.put("/cart/items/{item_id}", response_model=cartitems.CartResponse)
def update_cart_item(item_id: int, req: cartitems.UpdateCartItem, db: Session = Depends(get_db)):
	item = user_methods.update_cart_item(db, item_id, req)
	if item is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
	return item


@router.delete("/cart/items/{item_id}", response_model=cartitems.CartResponse)
def delete_cart_item(item_id: int, db: Session = Depends(get_db)):
	item = user_methods.delete_cart_item(db, item_id)
	if item is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
	return item