from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)

from database.config import get_session

from schema import Success
from schema.tourist_spot import FavoriteTouristSpotPagedSchema

from service.authentication import JWT, JWTExceptionExpired
from service.user import UserService

from controller.authentication import api_key_authorization

router = APIRouter()


@router.get(
    "/me/favoriteTouristSpot",
    status_code=HTTP_200_OK,
    response_model=FavoriteTouristSpotPagedSchema
)
def get_favorite_tourist_spot(
    offset: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    authorization: str = Depends(api_key_authorization), 
) -> FavoriteTouristSpotPagedSchema:
    try:
        token = JWT().validate(authorization)
    except JWTExceptionExpired:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Recurso não autorizado'
        )

    user_service = UserService(session)
    user = user_service.get_by_email(token['email'])

    favorites = user_service.get_favorite_tourist_spots(offset, limit, user.id)

    return FavoriteTouristSpotPagedSchema(
        items=favorites,
        total=len(favorites)
    )


@router.delete(
    "/me/favoriteTouristSpot/{id}",
    status_code=HTTP_200_OK,
    response_model=Success
)
def delete_favorite_tourist_spot(
    tourist_spot_id: int = 100, 
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

    return Success(
        message='Ponto turistico favorito removido com sucesso'
    )