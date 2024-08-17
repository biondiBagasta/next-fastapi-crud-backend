
from schemas.user_schema import User, UserCreateDto, UserUpdateDto
from database import models
from sqlalchemy.orm import Session
from sqlalchemy import delete, insert, exc, update
from fastapi import Depends, APIRouter
from database.db import get_db
from typing import List
from schemas.response_query_schema import ResponseQuery
import bcrypt

from utils.utils import authGuard

# Hash a password using bcrypt
def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode()

router = APIRouter(dependencies=[Depends(authGuard)])

@router.get("/many")
def findMany(db: Session = Depends(get_db)) -> List[User]:
	queryData = db.query(models.User).order_by(models.User.full_name.asc()).all()
	return list(queryData)

@router.post("/")
def createData(body: UserCreateDto, db: Session = Depends(get_db)) -> ResponseQuery:
	hashedPassword = hash_password(body.password)

	try:
		with db.begin():
			queryInsert = db.execute(insert(models.User).values(
				UserCreateDto(
					username=body.username,
					password=hashedPassword,
					full_name=body.full_name,
					address=body.address,
					phone_number=body.phone_number,
					role=body.role
				).model_dump()
			))

			return ResponseQuery(status=True, message=f"User Data {body.full_name} was Created.")
	except exc.SQLAlchemyError as e:
		print(f"{str(e)}")
		db.rollback()

		return ResponseQuery(status=False, message=f"Failed to Create User Data.")

@router.put("/{id}")
def updateData(id: str, body: UserUpdateDto, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			if(body.password != None or body.password != ""):
				hashedNewPassword = hash_password(body.password or "")
				queryUpdate = db.execute(update(models.User).values(body.model_dump(exclude_unset=True))
					.where(models.User.id == int(id)))
				return ResponseQuery(status=True, message=f"User Data {body.full_name} was Updated.")
			else:
				queryUpdate = db.execute(update(models.User).values(body.model_dump(exclude_unset=True))
					.where(models.User.id == int(id)))
				return ResponseQuery(status=True, message=f"User Data {body.full_name} was Updated.")
	except exc.SQLAlchemyError as e:
		print(f"{str(e)}")
		db.rollback()

		return ResponseQuery(status=False, message=f"Failed to Update User Data")

@router.delete("/{id}")
def deleteData(id: str, db: Session = Depends(get_db)) -> ResponseQuery:
	db.execute(delete(models.User).where(models.User.id == int(id)))

	db.commit()

	return ResponseQuery(status=True, message="User Data was Deleted.")
