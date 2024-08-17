from typing import Iterable
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import delete, exc, insert, select, update
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.paginate_schema import Paginate
from schemas.product_schema import Product, ProductCreateDto, ProductUpdateDto, ProductPaginateResponse
from schemas.response_query_schema import ResponseQuery
from database import models
from utils.utils import authGuard

router = APIRouter(dependencies=[Depends(authGuard)])

@router.get("/many")
def findMany(db: Session = Depends(get_db)) -> list[Product]:
	queryFindFirst = db.query(models.Product).scalar()
	print(queryFindFirst)
	queryFindMany = db.execute(
		select(models.Product).select_from(models.Product)\
		.join(models.Category, models.Product.category_id == models.Category.id)\
		.order_by(models.Product.name)
	).scalars().all()
	return list(queryFindMany)


@router.get("/search/")
def searchPaginate(page: int = 10, term: str = "", db: Session = Depends(get_db)) -> ProductPaginateResponse:
	pageTake = 10

	queryCount = db.query(models.Product).filter(models.Product.name.ilike(f"%{term}%")).count()

	# querySearch = db.query(models.Product).filter(models.Product.name.ilike(f"%{term}%"))\
	# .order_by(models.Product.name.asc()).limit(pageTake).offset((page - 1) * pageTake).all()
	querySearch = db.execute(select(models.Product).join(models.Category, models.Product.category_id == models.Category.id) \
	.filter(models.Product.name.ilike(f"%{term}%")).order_by(models.Product.name.asc())\
	.limit(pageTake).offset((page - 1) * pageTake)).scalars().all()

	totalPage = round((queryCount / pageTake) + 0.4)

	# return list(querySearch)

	return ProductPaginateResponse(
		data=list(querySearch),
		paginate=Paginate(
			per_page=10,
			total_page=totalPage,
			count=queryCount,
			current_page=page
		)
	)

@router.post("/")
def createData(body: ProductCreateDto, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			db.execute(
				insert(models.Product).values(body.model_dump())
			)

			return ResponseQuery(
				status=True,
				message=f"Product {body.name} data was created."
			)
	except exc.SQLAlchemyError as e:
		print(f"{str(e)}")
		db.rollback()

		return ResponseQuery(
			status=False,
			message="Failed to create Product data."
		)

@router.put("/{id}")
def updateData(id: str, body: ProductUpdateDto, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			queryUpdate = db.execute(
				update(models.Product).values(body.model_dump(exclude_unset=True)).where(
					models.Product.id == int(id)
				)
			)

			return ResponseQuery(
				status=True,
				message=f"Product {body.name} data was updated."
			)
	except exc.SQLAlchemyError as e:
		print(f"{str(e)}")
		db.rollback()

		return ResponseQuery(
			status=False,
			message="Failed to update Product data."
		)

@router.delete("/{id}")
def deleteData(id: str, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			queryDelete = db.execute(
				delete(models.Product).where(models.Product.id == int(id))
			)

			return ResponseQuery(
				status=True,
				message=f"Product data was deleted."
			)
	except exc.SQLAlchemyError as e:
		print(f"{str(e)}")

		db.rollback()

		return ResponseQuery(
			status=False,
			message="Failed to delete Product data."
		)