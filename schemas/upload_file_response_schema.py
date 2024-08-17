
from pydantic import BaseModel, ConfigDict


class UploadFileResponse(BaseModel):
	filename: str
	extension: str

	model_config =  ConfigDict(from_attributes=True)