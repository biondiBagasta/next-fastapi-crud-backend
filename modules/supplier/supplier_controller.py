
from fastapi import APIRouter, Depends
from sqlalchemy import delete, exc, insert, select, update
from sqlalchemy.orm import Session

from database import models
from database.db import get_db
from schemas.paginate_schema import Paginate
from schemas.response_query_schema import ResponseQuery
from schemas.supplier_schema import SupplierCreateDto, SupplierPaginateResponse, SupplierUpdateDto
from utils.utils import authGuard


router = APIRouter(dependencies=[Depends(authGuard)])

@router.get("/search/")
def searchPaginate(page: int = 10, term: str = "", db: Session = Depends(get_db)) -> SupplierPaginateResponse:
	pageTake = 10
	queryCount = db.query(models.Supplier).filter(models.Supplier.name.ilike(f"%{term}%")).count()
	querySearch = db.execute(
		select(models.Supplier).filter(models.Supplier.name.ilike(f"%{term}%"))\
		.limit(pageTake).offset((page - 1) * pageTake)
	).scalars().all()

	totalPage = round((queryCount / pageTake) + 0.4)

	return SupplierPaginateResponse(
		data=list(querySearch),
		paginate=Paginate(
			per_page=pageTake,
			total_page=totalPage,
			count=queryCount,
			current_page=page
		)
	)

@router.post("/")
def createData(body: SupplierCreateDto, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			db.execute(
				insert(models.Supplier).values(body.model_dump())
			)

			return ResponseQuery(
				status=True,
				message=f"Supplier {body.name} data was created."
			)
	except exc.SQLAlchemyError as e:
		print(f"{str(e)}")

		return ResponseQuery(
			status=False,
			message="Failed to create Supplier data."
		)

@router.put("/{id}")
def updateData(id: str, body: SupplierUpdateDto, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			db.execute(
				update(models.Supplier).values(body.model_dump()).where(
					models.Supplier.id == int(id)
				)
			)

			return ResponseQuery(
				status=True,
				message=f"Supplier data was updated."
			)
	except exc.SQLAlchemyError as e:
		return ResponseQuery(
			status=False,
			message="Falied to update Supplier data."
		)

@router.delete("/{id}")
def deleteData(id: str, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			db.execute(
				delete(models.Supplier).where(models.Supplier.id == int(id))
			)

			return ResponseQuery(
				status=True,
				message="Supplier data was deleted."
			)
	except exc.SQLAlchemyError as e:
		return ResponseQuery(
			status=False,
			message="Failed to delete Supplier data."
		)