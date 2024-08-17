from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.db import SessionLocal, engine
from database import models
from modules.auth import auth_controller
from modules.category import category_controller
from modules.files import files_controller
from modules.product import product_controller
from modules.user import user_controller

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
	"http://localhost:3000"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True
)

app.include_router(user_controller.router, tags=["User"], prefix="/api/user")
app.include_router(auth_controller.router, tags=["Auth"], prefix="/api/auth")
app.include_router(category_controller.router, tags=["Category"], prefix="/api/category")
app.include_router(product_controller.router, tags=["Product"], prefix="/api/product")
app.include_router(files_controller.router, tags=["Files"], prefix="/api/files")

if __name__ == "__main__":
	import uvicorn

	uvicorn.run("__main__:app", host="0.0.0.0", port=8200, workers=2, reload=True)