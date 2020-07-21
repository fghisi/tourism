from fastapi import APIRouter

from controller import authentication

router = APIRouter()
router.include_router(authentication.router)