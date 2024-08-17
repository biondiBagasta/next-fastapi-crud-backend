from schemas.auth_schema import LoginBody, LoginResponse
from schemas.user_schema import User
from database import models
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends, APIRouter, HTTPException, Request
from database.db import get_db
import jwt
from utils.utils import JWT_SECRET, JWT_ALGORITHM, authGuard
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password.encode("utf-8"))

router = APIRouter()

@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)) -> LoginResponse:
	queryFindFirstUser = db.query(models.User).filter(models.User.username == body.username).first()

	if not queryFindFirstUser:
		raise HTTPException(status_code=404, detail="User Not Found!!!")
	else:
		convertedQueryToUser = User.model_validate(queryFindFirstUser)
		comparePassword = verify_password(body.password, convertedQueryToUser.password)

		print(convertedQueryToUser)
		if(comparePassword == False):
			raise HTTPException(status_code=404, detail="User Not Found!!!")
		else:
			encodedJwt = jwt.encode(convertedQueryToUser.model_dump(mode="json"), JWT_SECRET, algorithm=JWT_ALGORITHM)

			return LoginResponse(
				user=convertedQueryToUser,
				token = encodedJwt
			)

@router.post("/authenticated", dependencies=[Depends(authGuard)])
def authenticated(request: Request) -> LoginResponse:
	authorization = request.headers["Authorization"]
	token = authorization.replace("Bearer ", "")
	
	try:
		decodedToken = jwt.decode(jwt=token, algorithms=[JWT_ALGORITHM], key=JWT_SECRET)
		decodedUserData = User.parse_obj(decodedToken)
		
		newToken = jwt.encode(decodedUserData.model_dump(mode="json"), JWT_SECRET, algorithm=JWT_ALGORITHM)

		return LoginResponse(
			user=decodedUserData,
			token=newToken
		)
	except jwt.InvalidTokenError:
		raise HTTPException(status_code=403, detail="Token was Expired")
