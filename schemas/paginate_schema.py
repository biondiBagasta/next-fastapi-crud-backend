
from pydantic import BaseModel

class Paginate(BaseModel):
	per_page: int
	total_page: int
	count: int
	current_page: int