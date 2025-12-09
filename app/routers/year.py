from fastapi import APIRouter
from ..services.entries import get_entry_by_year
from ..services.years import get_years

router = APIRouter()


@router.get("/years/", tags=["years"])
async def read_years():
    return get_years()


@router.get("/year/{year}", tags=["years"])
async def read_specific_year(year: str):
    return get_entry_by_year(year)
