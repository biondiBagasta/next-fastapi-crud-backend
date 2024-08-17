from fastapi import HTTPException, Request, status
import jwt

JWT_SECRET = "SEMANGATBELAJARFASTAPI"
JWT_ALGORITHM = "HS256"

async def authGuard(request: Request):
	if "authorization" not in request.headers.keys():
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")
	else:
		try:
			authorization = request.headers["Authorization"]
			token = authorization.replace("Bearer ", "")
			decodedToken = jwt.decode(jwt=token, algorithms=[JWT_ALGORITHM], key=JWT_SECRET)
		except jwt.InvalidTokenError:
			raise HTTPException(status_code=403, detail="Token was Expired")
