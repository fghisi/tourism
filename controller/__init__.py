from fastapi import APIRouter

from controller import authentication
from controller import category
from controller import tourist_spot
from controller import me

router = APIRouter()
router.include_router(authentication.router)
router.include_router(category.router)
router.include_router(tourist_spot.router)
router.include_router(me.router)