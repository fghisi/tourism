from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND
)

from database.config import get_session

from schema import ObjectCreate
from schema.user import UserSchema

from service.user import UserService
from service.authentication import AuthenticationService, EmailOrPasswordInvalid

router = APIRouter()


@router.post(
    "/signup",
    status_code=HTTP_201_CREATED,
    response_model=ObjectCreate
)
def signup(
    user_schema: UserSchema = Body(..., embed=True, alias="user"),
    session: Session = Depends(get_session),
) -> ObjectCreate:
    user_service = UserService(session)

    if user_service.get_by_email(user_schema.email):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Usuário já criado'
        )

    user = user_service.insert(user_schema.dict())

    return ObjectCreate(
        message='Usuário criado com sucesso',
        object_id=user.id
    )


@router.post(
    "/login",
    status_code=HTTP_200_OK
)
def login(
    user_schema: UserSchema = Body(..., embed=True, alias="user"),
    session: Session = Depends(get_session),
):
    user_service = UserService(session)
    auth_service = AuthenticationService(session)

    if not user_service.get_by_email(user_schema.email):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='E-mail não encontrado'
        )
    
    try:
        token = auth_service.get_token(
            user_schema.email,
            user_schema.password
        )
    except EmailOrPasswordInvalid:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='E-mail ou senha inválido'
        )

    return {
        'message': 'Login efetuado',
        'token': token
    }


api_key_authorization = APIKeyHeader(name='authorization')