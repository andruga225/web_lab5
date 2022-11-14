from fastapi import APIRouter

from app.modules.dictionary.api import router as dictionary_router


router = APIRouter()

router.include_router(dictionary_router, prefix="/v1")