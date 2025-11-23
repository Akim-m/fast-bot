from fastapi import APIRouter, HTTPException
from services.db_service import get_table_data, list_tables

router = APIRouter(prefix="/db", tags=["Database"])

@router.get("/")
def get_all_tables():

    tables = list_tables()
    return {"tables": tables}

@router.get("/{table_name}")
def get_table_rows(table_name: str):
    try:
        rows = get_table_data(table_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"table": table_name, "rows": rows}
