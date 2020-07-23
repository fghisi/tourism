from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND
)

from database.config import get_session

from schema import ObjectCreate, Success
from schema.tourist_spot import TouristSpotSchema, TouristSpotPagedSchema, ImageSchema

from service.authentication import JWT, JWTExceptionExpired
from service.tourist_spot import TouristSpotService
from service.favorite_tourist_spot import FavoriteTouristSpotService
from service.user import UserService

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

@router.get(
    "/touristSpot",
    status_code=HTTP_200_OK,
    response_model=TouristSpotPagedSchema
)
def get_tourist_spot(
    offset: int = 0, 
    limit: int = 100, 
    name: str = None,
    session: Session = Depends(get_session),
    authorization: str = Depends(api_key_authorization), 
) -> TouristSpotPagedSchema:
    try:
        JWT().validate(authorization)
    except JWTExceptionExpired:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Recurso não autorizado'
        )

    tourist_spot_service = TouristSpotService(session)
    tourist_spots = tourist_spot_service.get(offset, limit, name)
    
    return TouristSpotPagedSchema(
        items=tourist_spots,
        total=len(tourist_spots)
    )


@router.post(
    "/touristSpot/{id}/favorite",
    status_code=HTTP_200_OK,
    response_model=Success
)
def post_favorite_tourist_spot(
    id: int,
    session: Session = Depends(get_session),
    authorization: str = Depends(api_key_authorization), 
) -> Success:
    try:
        token = JWT().validate(authorization)
    except JWTExceptionExpired:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Recurso não autorizado'
        )

    user_service = UserService(session)
    user = user_service.get_by_email(token['email'])

    tourist_spot_service = TouristSpotService(session)

    try:
        tourist_spot = tourist_spot_service.get_by_id(id)
    except NoResultFound:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Ponto turistico não encontrado'
        )

    favorite_service = FavoriteTouristSpotService(session)
    favorite_service.insert({
        'user_id': user.id,
        'tourist_spot_id': tourist_spot.id
    })

    return Success(
        message='Ponto turistico favoritado com sucesso'
    )

@router.put(
    "/touristSpot/{id}/image",
    status_code=HTTP_200_OK,
    response_model=Success
)
def put_tourist_spot_image(
    id: int,
    image_schema: ImageSchema = Body(..., embed=True, alias="image"),
    session: Session = Depends(get_session),
    authorization: str = Depends(api_key_authorization), 
) -> Success:
    try:
        JWT().validate(authorization)
    except JWTExceptionExpired:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Recurso não autorizado'
        )

    tourist_spot_service = TouristSpotService(session)
    tourist_spot_service.update_image(id, image_schema.image)

    return Success(
        message='Imagem atualizada com sucess favoritado com sucesso'
    )