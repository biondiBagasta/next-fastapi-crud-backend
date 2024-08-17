
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class User(BaseModel):
	id: int
	username: str
	password: str
	full_name: str
	address: str
	phone_number: str
	role: str
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(from_attributes=True, json_encoders={
		datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')
	})

class UserCreateDto(BaseModel):
	username: str
	password: str
	full_name: str
	address: str
	phone_number: str
	role: str

class UserUpdateDto(BaseModel):
	username: str | None
	password: str | None
	full_name: str | None
	address: str | None
	phone_number: str | None
	role: str | None