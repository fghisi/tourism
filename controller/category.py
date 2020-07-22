from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from database.config import get_session

from schema import ObjectCreate
from schema.category import CategorySchema

from service.authentication import JWT, JWTExceptionExpired
from service.category import CategoryService

from controller.authentication import api_key_authorization

router = APIRouter()


@router.post(
    "/category",
    status_code=HTTP_201_CREATED,
    response_model=ObjectCreate
)
def post_category(
    category_schema: CategorySchema = Body(..., embed=True, alias="category"),
    session: Session = Depends(get_session),
    authorization: str = Depends(api_key_authorization), 
) -> ObjectCreate:
    try:
        JWT().validate(authorization)
    except JWTExceptionExpired:
        pass

    category_service = CategoryService(session)

    if category_service.get_by_name(category_schema.name):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Categoria já criada'
        )

    category = category_service.insert(category_schema.dict())

    return ObjectCreate(
        message='Categoria criada com sucesso',
        object_id=category.id
    )