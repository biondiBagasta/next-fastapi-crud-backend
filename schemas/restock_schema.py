
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from schemas.paginate_schema import Paginate

class Product(BaseModel):
	name: str
	purchase_price: int
	qty: int

	model_config = ConfigDict(from_attributes=True)

class RestockDetail(BaseModel):
	supplier: str
	products: list[Product]

	model_config = ConfigDict(from_attributes=True)

class Restock(BaseModel):
	id: int
	restock_date: datetime
	amount: int
	detail: str
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(from_attributes=True)


class RestockPaginate(BaseModel):
	data: list[Restock]
	paginate: Paginate

class RestockCreateDto(BaseModel):
	restock_date: datetime
	amount: int
	detail: str

class RestockUpdateDto(BaseModel):
	restock_date: datetime | None
	amount: int  | None
	deetail: str | None

