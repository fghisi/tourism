from fastapi import APIRouter, Body
from starlette.status import HTTP_201_CREATED

from schema.user import User

router = APIRouter()


@router.post(
    "/signin",
    status_code=HTTP_201_CREATED
)
async def signin(
    user_create: User = Body(..., embed=True, alias="user")
):
    import pdb; pdb.set_trace()
    return 'Ola'