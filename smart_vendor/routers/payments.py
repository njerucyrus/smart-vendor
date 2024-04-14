import json
import os
from pprint import pprint

from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi_pagination.links import Page
from sqlalchemy.orm import Session
from starlette import status

from mpesa.mpesa_express import MpesaExpress
from mpesa.utils import PhoneNumberUtils
from smart_vendor import schemas
from smart_vendor.db_services.payments import db_create_payment, \
    db_get_payment, db_update_payment, \
    db_list_payments, db_patch_payment, \
    db_delete_payment
from smart_vendor.db_services.user_accounts import db_get_user_account
from smart_vendor.dependancies import get_db_session
from dotenv import load_dotenv

load_dotenv()
api_base_url = os.environ.get('API_BASE_URL')

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
async def send_stk_push(body: schemas.STKPushRequest, response: Response, db: Session = Depends(get_db_session)):
    account = await db_get_user_account(
        db=db,
        card_id=body.account_number
    )

    if account:
        mpesa_client = MpesaExpress()
        res = mpesa_client.stk_push(
            amount=body.amount,
            phone_number=PhoneNumberUtils.clean(body.phone_number),
            description="Top up",
            reference_code=body.account_number,
            callback_url=f"{api_base_url}/payments/test-callback/"
        )
        data = schemas.StkRequestResponse(**dict(res))
        if data.response_code == "0":
            # request sent successfully. we create a new payment entry
            payment_payload = {
                'account_id': account.id,
                'txn_id': data.checkout_request_id,
                'amount': round(float(body.amount), 2),
                'phone_number': PhoneNumberUtils.clean(body.phone_number),
                'status': 'pending'
            }
            payment = schemas.PaymentCreate(
                **payment_payload
            )
            payment_record = await db_create_payment(db, payment)
            response.status_code = status.HTTP_200_OK
            return {
                'message': data.customer_message,
                'txn_id': payment_record.txn_id
            }
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                'message': data.customer_message
            }
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': 'Invalid account number. Make sure you use your CardID as the account number'
        }


@router.post("/payments/callback/")
async def payment_callback(payload: schemas.StkPayload, response: Response, db:Session = Depends(get_db_session)):
    stk_callback = payload.Body.stkCallback
    with(open('callback.json', 'w+')) as f:
        f.write(json.dumps(payload.model_dump()))
    if str(stk_callback.ResultCode) == '0':

        processed_data = {
            "CheckoutRequestId": stk_callback.CheckoutRequestID,
            "ResultCode": stk_callback.ResultCode,
            "ResultDesk": stk_callback.ResultDesc,
            "MpesaReceiptNumber": next(
                (str(item.Value) for item in stk_callback.CallbackMetadata.Item if item.Name == "MpesaReceiptNumber"),
                None),
            "PhoneNumber": next(
                (str(item.Value) for item in stk_callback.CallbackMetadata.Item if item.Name == "PhoneNumber"),
                None),
            "Amount": next(
                (round(float(item.Value), 2) for item in stk_callback.CallbackMetadata.Item if item.Name == "Amount"),
                None),
        }

        payload_schema = {
            'txn_id': str(processed_data.get('CheckoutRequestId')),
            'amount': processed_data.get('Amount'),
            'receipt_no': processed_data.get('MpesaReceiptNumber'),
            'status': 'success'

        }
        patch_schema = schemas.PaymentUpdate(**payload_schema)
        txn = await db_patch_payment(
            db=db,
            txn_id=str(processed_data.get('CheckoutRequestId')),
            payment=patch_schema

        )
        response.status_code = status.HTTP_200_OK
        return txn

    else:
        # payment failed
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'message': stk_callback.ResultDesc,
            'status': 'failed'
        }

    return processed_data


@router.post("/payments/test-callback/")
async def test_callback(data:dict):
    with(open('test_callback.json', 'w+')) as f:
        f.write(json.dumps(data))

    return  {'status': 'completed'}
