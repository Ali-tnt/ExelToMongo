from fastapi import APIRouter, UploadFile, HTTPException
from app.database import collection
from app.models import PhoneNumber, PhoneNumberUpdate, UploadResponse
import pandas as pd
import time
from bson import ObjectId
from typing import List

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_excel(file: UploadFile):
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="File must be an Excel file")

    start_time = time.time()

    # Read Excel file
    df = pd.read_excel(file.file)

    if 'mobile' not in df.columns:
        raise HTTPException(status_code=400, detail="Excel file must contain 'mobile' column")

    # Convert DataFrame to list of dictionaries
    records = df.to_dict('records')

    # Insert records into MongoDB
    await collection.insert_many(records)

    processing_time = time.time() - start_time

    return UploadResponse(
        total_records=len(records),
        processing_time=processing_time,
        message="File processed successfully"
    )


@router.get("/phones", response_model=List[PhoneNumber])
async def get_all_phones():
    phones = await collection.find().to_list(length=None)
    return [{**phone, "_id": str(phone["_id"])} for phone in phones]


@router.get("/phones/{phone_id}", response_model=PhoneNumber)
async def get_phone(phone_id: str):
    phone = await collection.find_one({"_id": ObjectId(phone_id)})
    if phone:
        return {**phone, "_id": str(phone["_id"])}
    raise HTTPException(status_code=404, detail="Phone number not found")


@router.put("/phones/{phone_id}", response_model=PhoneNumber)
async def update_phone(phone_id: str, phone: PhoneNumberUpdate):
    update_result = await collection.update_one(
        {"_id": ObjectId(phone_id)},
        {"$set": phone.dict(exclude_unset=True)}
    )

    if update_result.modified_count:
        updated_phone = await collection.find_one({"_id": ObjectId(phone_id)})
        return {**updated_phone, "_id": str(updated_phone["_id"])}
    raise HTTPException(status_code=404, detail="Phone number not found")


@router.delete("/phones/{phone_id}")
async def delete_phone(phone_id: str):
    delete_result = await collection.delete_one({"_id": ObjectId(phone_id)})
    if delete_result.deleted_count:
        return {"message": "Phone number deleted successfully"}
    raise HTTPException(status_code=404, detail="Phone number not found")