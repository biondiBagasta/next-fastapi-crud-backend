from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from schemas.paginate_schema import Paginate

class Product(BaseModel):
	id: int
	code: str
	name: str
	purchase_price: int
	selling_price: int
	stock: int
	discount: int
	image: str
	category_id: int
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(from_attributes=True)

class Category(BaseModel):
	id: int
	name: str
	created_at: datetime
	updated_at: datetime
	products: list[Product] = []

	model_config = ConfigDict(from_attributes=True)

class CategoryCreateDto(BaseModel):
	name: str

class CategoryUpdateDto(BaseModel):
	name: str | None

class CategoryPaginateResponse(BaseModel):
	data: List[Category]
	paginate: Paginate
