from pydantic import BaseModel, ConfigDict
from schemas.user_schema import User

class LoginBody(BaseModel):
	username: str
	password: str

class LoginResponse(BaseModel):
	user: User
	token: str

	model_config =  ConfigDict(from_attributes=True)

