from fastapi import Depends, APIRouter
from fastapi.responses import Response
from sqlalchemy.orm import Session

from smart_vendor.dependancies import get_db_session

router = APIRouter()


@router.post("/dispense/")
async def dispense(card_id:str, amount:int, response:Response, db:Session = Depends(get_db_session)):
    pass