from fastapi import APIRouter
from app.services.data_service import get_all_suppliers, get_summary

router = APIRouter(prefix="/risk", tags=["Risk Assessment"])

@router.get("/suppliers")
def suppliers():
    return get_all_suppliers()

@router.get("/summary")
def summary():
    return get_summary()