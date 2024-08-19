from sqlalchemy import ForeignKey, Integer, String, Column, DateTime, DECIMAL, Text
from datetime import datetime

from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	username = Column(String(50), nullable=False)
	password = Column(String(255), nullable=False)
	full_name = Column(String(50), nullable=False)
	address = Column(String(255), nullable=False)
	phone_number = Column(String(20), nullable=False)
	role = Column(String(20), nullable=False)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, default=datetime.now())

class Category(Base):
	__tablename__ = "category"

	id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(50), nullable=False)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, default=datetime.now())
	products = relationship("Product", back_populates="category", lazy="noload")

class Product(Base):
	__tablename__ = "product"

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	code = Column(String(100), nullable=False)
	name = Column(String(100), nullable=False)
	purchase_price = Column(DECIMAL(precision=2, scale=15), nullable=False)
	selling_price = Column(DECIMAL(precision=2, scale=15), nullable=False)
	stock = Column(Integer, nullable=False)
	discount = Column(Integer, nullable=False)
	image = Column(String(255), nullable=False)
	category_id = Column(Integer, ForeignKey("category.id"))
	category = relationship("Category", back_populates="products", foreign_keys=[category_id], lazy='joined')
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, default=datetime.now())

class Supplier(Base):
	__tablename__ = "supplier"

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	name = Column(String(50), nullable=False)
	address = Column(String(255), nullable=False)
	phone_number = Column(String(20), nullable=False)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, default=datetime.now())

class Restock(Base):
	__tablename__ = "restock"

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
	restock_date = Column(DateTime, nullable=False)
	amount = Column(Integer, nullable=False)
	detail = Column(Text, nullable=False)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, default=datetime.now())