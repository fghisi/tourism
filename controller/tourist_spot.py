from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from database.config import get_session

from schema import ObjectCreate
from schema.tourist_spot import TouristSpotSchema

from service.authentication import JWT, JWTExceptionExpired
from service.tourist_spot import TouristSpotService

from controller.authentication import api_key_authorization

router = APIRouter()


@router.post(
    "/touristSpot",
    status_code=HTTP_201_CREATED,
    response_model=ObjectCreate
)
def post_tourist_spot(
    tourist_spot_schema: TouristSpotSchema = Body(..., embed=True, alias="turist_spot"),
    session: Session = Depends(get_session),
    authorization: str = Depends(api_key_authorization), 
) -> ObjectCreate:
    try:
        JWT().validate(authorization)
    except JWTExceptionExpired:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Recurso não autorizado'
        )

    tourist_spot_service = TouristSpotService(session)

    if tourist_spot_service.get_by_name(tourist_spot_schema.name):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Ponto turistico já criado'
        )

    tourist_spot = tourist_spot_service.insert(tourist_spot_schema.dict())

    return ObjectCreate(
        message='Ponto turistico criado com sucesso',
        object_id=tourist_spot.id
    )