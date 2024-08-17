from pydantic import BaseModel

class ResponseQuery(BaseModel):
	status: bool
	message: str