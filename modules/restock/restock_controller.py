
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, session
from sqlalchemy import delete, exc, insert, update, values
from database import models
from database.db import get_db
from schemas.paginate_schema import Paginate
from schemas.response_query_schema import ResponseQuery
from schemas.restock_schema import RestockCreateDto, RestockDetail, RestockPaginate, RestockUpdateDto
from utils.utils import authGuard


router = APIRouter(dependencies=[Depends(authGuard)])

@router.get("/paginate")
def paginate(page: int = 1, db: Session = Depends(get_db)) -> RestockPaginate:
	pageTake = 10

	queryCount = db.query(models.Restock).count()
	querySelect = db.query(models.Restock).limit(pageTake).offset((page - 1) * pageTake).all()

	totalPage = round((queryCount / pageTake) + 0.4)

	return RestockPaginate(
		data=list(querySelect),
		paginate=Paginate(
			per_page=pageTake,
			total_page=totalPage,
			count=queryCount,
			current_page=page
		)
	)

@router.post("/filter-by-date")
def filterByDate(page: int, start_date: date, end_date: date,
	db: Session = Depends(get_db)) -> RestockPaginate:
	pageTake = 10

	queryCount = db.query(models.Restock).count()
	queryFilter = db.query(models.Restock).filter(models.Restock.restock_date.between(start_date, end_date)) \
	.order_by(models.Restock.restock_date.desc()).limit(pageTake).offset((page - 1) * pageTake).all()

	totalPage = round((queryCount / pageTake) + 0.4)

	return RestockPaginate(
		data=list(queryFilter),
		paginate=Paginate(
			per_page=pageTake,
			total_page=totalPage,
			count=queryCount,
			current_page=page
		)
	)

@router.post("/")
def createData(body: RestockCreateDto, db: Session = Depends(get_db)) -> ResponseQuery:
	parsedDetail = RestockDetail.model_validate_json(body.detail)

	try:
		with db.begin():
			db.execute(insert(models.Restock).values(body.model_dump()))

			for d in parsedDetail.products:
				queryFindFirstProduct = db.query(models.Product).where(models.Product.name == d.name).one()

				db.execute(update(models.Product).values(
					stock = queryFindFirstProduct.stock + d.qty
				).where(models.Product.id == queryFindFirstProduct.id))

			return ResponseQuery(
				status=True,
				message="Restock data was created."
			)
			
	except exc.SQLAlchemyError as e:
		db.rollback()

		return ResponseQuery(
			status=False,
			message="Failed to create Restock data."
		)

	return ResponseQuery(status=True, message="TEST BODY")

# @router.put("/{id}")
# def updateData(id: str, body: RestockUpdateDto, db: Session = Depends(get_db)) -> ResponseQuery:
# 	print(body)

# 	return ResponseQuery(status=True, message="Test Body")

@router.delete("/{id}")
def deleteData(id: str, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			db.execute(delete(models.Restock).where(models.Restock.id == int(id)))

			return ResponseQuery(
				status=True,
				message="Restock data was deleted."
			)

	except exc.SQLAlchemyError as e:
		db.rollback()

		return ResponseQuery(
			status=True,
			message="Failed to delete Restock data."
		)