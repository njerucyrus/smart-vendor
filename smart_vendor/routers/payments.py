from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi_pagination.links import Page
from sqlalchemy.orm import Session
from starlette import status

from smart_vendor import schemas
from smart_vendor.db_services.payments import db_create_payment, \
    db_get_payment, db_update_payment, \
    db_list_payments, db_patch_payment, \
    db_delete_payment
from smart_vendor.dependancies import get_db_session

router = APIRouter()


@router.post("/payments/", response_model=schemas.PaymentRead)
async def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db_session)):
    instance = await db_create_payment(db, payment)
    return instance


@router.get("/payments/")
async def get_payments(db: Session = Depends(get_db_session)) -> Page[schemas.PaymentRead]:
    payments = await db_list_payments(db)
    return payments


@router.get("/payments/{txn_id}/", response_model=schemas.PaymentRead)
async def payment_detail(txn_id: str, db: Session = Depends(get_db_session)):
    payment = await db_get_payment(db, txn_id)
    return payment


@router.put("/payments/{txn_id}/", response_model=schemas.PaymentRead)
async def update_payment(txn_id: str, payment: schemas.PaymentUpdate, db: Session = Depends(get_db_session)):
    instance = await db_update_payment(db, txn_id, payment)
    return instance


@router.patch("/payments/{txn_id}/", response_model=schemas.PaymentRead)
async def partial_update_payment(txn_id: str, topup: schemas.PaymentUpdate, db: Session = Depends(get_db_session)):
    instance = await db_patch_payment(db, txn_id, topup)
    return instance


@router.delete("/payments/{txn_id}/")
async def delete_payment(txn_id: str, response: Response, db: Session = Depends(get_db_session)):
    deleted = await db_delete_payment(db, txn_id)
    if deleted is not None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'detail': 'Could not find matching transaction'
        }


@router.post("/payments/send-stk-push/")
async def send_stk_push(body: schemas.STKPushRequest, response: Response):
    return body


@router.post("/payments/callback/")
async def payment_callback(data: schemas.StkResponseBody, response:Response):
    stk_callback = data.Body.stkCallback

    processed_data = {
        "CheckoutRequestId": stk_callback.CheckoutRequestID,
        "ResultCode": stk_callback.ResultCode,
        "ResultDesk": stk_callback.ResultDesc,
        "MpesaReceiptNumber": next(
            (item.Value for item in stk_callback.CallbackMetadata.Item if item.Name == "MpesaReceiptNumber"), None),
        "PhoneNumber": next((item.Value for item in stk_callback.CallbackMetadata.Item if item.Name == "PhoneNumber"),
                            None),
        "Amount": next((item.Value for item in stk_callback.CallbackMetadata.Item if item.Name == "Amount"), None)
    }
    return processed_data
