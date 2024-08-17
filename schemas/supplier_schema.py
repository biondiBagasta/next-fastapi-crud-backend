
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from schemas.paginate_schema import Paginate


class Supplier(BaseModel):
	id: int
	name: str
	address: str
	phone_number: str
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(from_attributes=True)

class SupplierCreateDto(BaseModel):
	name: str
	address: str
	phone_number: str

class SupplierUpdateDto(BaseModel):
	name: str | None
	address: str | None
	phone_number: str | None

class SupplierPaginateResponse(BaseModel):
	data: list[Supplier]
	paginate: Paginate