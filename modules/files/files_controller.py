from fastapi import APIRouter, Depends, UploadFile
import shutil
import os
import time
from fastapi.responses import FileResponse
from schemas.upload_file_response_schema import UploadFileResponse
from utils.utils import authGuard

router = APIRouter()

@router.post("/product", dependencies=[Depends(authGuard)])
def uploadProductImage(product_image: UploadFile) -> UploadFileResponse:
	now = round(time.time() * 1000)
	fileLocation = f"uploads/product/{now}_{product_image.filename}"
	with(open(fileLocation, "wb+")) as fileObject:
		shutil.copyfileobj(product_image.file, fileObject)
	return UploadFileResponse(
		filename=f"{now}_{product_image.filename}" or "",
		extension=product_image.content_type or ""
	)

@router.delete("/product/{filename}", dependencies=[Depends(authGuard)])
def deleteProductImage(filename: str):
	fileLocation = f"\\uploads\\product\\{filename}"
	dirname = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

	joinDirnameFileLocation = dirname + fileLocation
	print(fileLocation)

	if os.path.exists(joinDirnameFileLocation):
		os.unlink(joinDirnameFileLocation)

@router.get("/product/image/{filename}", response_class=FileResponse)
def getProductImage(filename: str):
	fileLocation = f"\\uploads\\product\\{filename}"
	dirname = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

	joinDirnameFileLocation = dirname + fileLocation

	print(joinDirnameFileLocation)

	return joinDirnameFileLocation