
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from schemas import paginate_schema
from schemas.paginate_schema import Paginate

class Category(BaseModel):
	id: int
	name: str
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(from_attributes=True)

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
	category: Category | None
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(from_attributes=True)

class ProductCreateDto(BaseModel):
	code: str
	name: str
	purchase_price: int
	selling_price: int
	stock: int
	discount: int
	image: str
	category_id: int

class ProductUpdateDto(BaseModel):
	code: str | None
	name: str | None
	purchase_price: int | None
	selling_price: int | None
	stock: int | None
	image: str | None
	category_id: int | None

class ProductPaginateResponse(BaseModel):
	data: list[Product]
	paginate: Paginate