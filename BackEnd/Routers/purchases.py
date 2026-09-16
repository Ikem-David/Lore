from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Database.DB_Methods import purchases as purchase_methods
from Database.db import get_db
from auth import get_current_user
from Schema import purchaseitems, purchases

router = APIRouter(
	prefix="/purchases",
	tags=['Purchases'],
	dependencies=[Depends(get_current_user)]
)

# Purchase Endpoints
@router.get("/", response_model=list[purchases.PurchaseResponse])
def read_purchases(db: Session = Depends(get_db)):
	return purchase_methods.get_all_purchases(db)


@router.get("/user/{user_id}", response_model=list[purchases.PurchaseResponse])
def read_user_purchases(user_id: int, db: Session = Depends(get_db)):
	return purchase_methods.get_user_purchases(db, user_id)


@router.get("/{purchase_id}", response_model=purchases.PurchaseResponse)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
	purchase = purchase_methods.get_purchase(db, purchase_id)
	if purchase is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
	return purchase


@router.post("/user/{user_id}", response_model=purchases.PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(user_id: int, req: purchases.PurchasesBase, db: Session = Depends(get_db)):
	return purchase_methods.create_purchase(db, user_id, req)


@router.put("/{purchase_id}", response_model=purchases.PurchaseResponse)
def update_purchase(purchase_id: int, req: purchases.PurchasesBase, db: Session = Depends(get_db)):
	purchase = purchase_methods.update_purchase(db, purchase_id, req)
	if purchase is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
	return purchase


@router.delete("/{purchase_id}", response_model=purchases.PurchaseResponse)
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
	purchase = purchase_methods.delete_purchase(db, purchase_id)
	if purchase is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
	return purchase

# Purchased Items Endpoints
@router.post("/items", response_model=purchaseitems.PurchaseItemResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_item(req: purchaseitems.CreatePurchaseItem, db: Session = Depends(get_db)):
	return purchase_methods.create_purchase_item(db, req)


@router.get("/items/{item_id}", response_model=purchaseitems.PurchaseItemResponse)
def read_purchase_item(item_id: int, db: Session = Depends(get_db)):
	item = purchase_methods.get_purchase_item(db, item_id)
	if item is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase item not found")
	return item


@router.get("/{purchase_id}/items", response_model=list[purchaseitems.PurchaseItemResponse])
def read_purchase_items(purchase_id: int, db: Session = Depends(get_db)):
	return purchase_methods.get_purchaseitems(db, purchase_id)


@router.put("/items/{item_id}", response_model=purchaseitems.PurchaseItemResponse)
def update_purchase_item(item_id: int, req: purchaseitems.UpdatePurchaseItem, db: Session = Depends(get_db)):
	item = purchase_methods.update_purchase_item(db, item_id, req)
	if item is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase item not found")
	return item


@router.delete("/items/{item_id}", response_model=purchaseitems.PurchaseItemResponse)
def delete_purchase_item(item_id: int, db: Session = Depends(get_db)):
	item = purchase_methods.delete_purchase_item(db, item_id)
	if item is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase item not found")
	return item