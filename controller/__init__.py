from fastapi import APIRouter

from controller import authentication
from controller import category

router = APIRouter()
router.include_router(authentication.router)
router.include_router(category.router)