
from fastapi import APIRouter, Depends
from sqlalchemy import delete, exc, insert, update
from sqlalchemy.orm import Session, lazyload
from database.db import get_db
from schemas.paginate_schema import Paginate
from utils.utils import authGuard
from schemas.category_schema import Category, CategoryCreateDto, CategoryUpdateDto, CategoryPaginateResponse
from schemas.response_query_schema import ResponseQuery
from database import models

router = APIRouter(dependencies=[Depends(authGuard)])

@router.get("/many")
def findMany(db: Session = Depends(get_db)) -> list[Category]:
	queryFindMany = db.query(models.Category)\
	.order_by(models.Category.name.asc()).all();
	return list(queryFindMany)


@router.get("/search/")
def searchPaginate(page: int = 1, term: str = "", db: Session = Depends(get_db)):
	pageTake = 10

	queryCount = db.query(models.Category).filter(models.Category.name.ilike(f"%{term}%")).count()
	querySearch = db.query(models.Category)\
	.filter(models.Category.name.ilike(f"%{term}%")).order_by(models.Category.name.asc()) \
	.limit(pageTake).offset((page - 1) * pageTake).all()

	totalPage = round((queryCount / pageTake) + 0.4)

	return CategoryPaginateResponse(
		data=list(querySearch),
		paginate=Paginate(
			per_page=pageTake,
			total_page=totalPage,
			count=queryCount,
			current_page=page
		)
	)

@router.post("/")
def createData(body: CategoryCreateDto, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			db.execute(
				insert(models.Category).values(body.model_dump())
			)

			return ResponseQuery(
				status=True,
				message=f"Category {body.name} data was created."
			)
	except exc.SQLAlchemyError as e:
		print(f"{str(e)}")
		db.rollback()

		return ResponseQuery(
			status=False,
			message="Failed to create Category data."
		)

@router.put("/{id}")
def updateData(id: str, body: CategoryUpdateDto, db: Session = Depends(get_db)) -> ResponseQuery:
	try:
		with db.begin():
			db.execute(
				update(models.Category).values(body.model_dump(exclude_unset=True)).where(
					models.Category.id == int(id)
				)
			)

			return ResponseQuery(
				status=True,
				message="Category data was updated."
			)
	except exc.SQLAlchemyError as e:
		print(f"{str(e)}")

		db.rollback()

		return ResponseQuery(
			status=False,
			message="Failed to update Category data."
		)

@router.delete("/{id}")
def deleteDdata(id: str, db: Session = Depends(get_db)) -> ResponseQuery:
	db.execute(delete(models.Category).where(models.Category.id == int(id)))

	db.commit()

	return ResponseQuery(
		status=True,
		message="Category data was deleted."
	)