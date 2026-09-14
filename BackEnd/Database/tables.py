from .db import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Relationships
    cart_items = relationship(
        "CartItem",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    purchases = relationship(
        "Purchases",
        back_populates="user"
    )


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String(500),nullable=False)
    categorie = Column(String(500),nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    # Relationships
    cart_items = relationship(
        "CartItem",
        back_populates="product"
    )

    purchase_items = relationship(
        "PurchaseItem",
        back_populates="product"
    )


class Purchases(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship(
        "Users",
        back_populates="purchases"
    )

    items = relationship(
        "PurchaseItem",
        back_populates="purchase",
        cascade="all, delete-orphan"
    )


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)

    purchase_id = Column(
        Integer,
        ForeignKey("purchases.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Relationships
    purchase = relationship(
        "Purchases",
        back_populates="items"
    )

    product = relationship(
        "Products",
        back_populates="purchase_items"
    )


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False, default=1)

    # Relationships
    user = relationship(
        "Users",
        back_populates="cart_items"
    )

    product = relationship(
        "Products",
        back_populates="cart_items"
    )