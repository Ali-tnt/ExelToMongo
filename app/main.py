from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import time
from typing import List
import io

from .database import init_db, collection
from .models import PhoneNumber, PhoneNumberUpdate, ProcessingResult

app = FastAPI(title="Excel to MongoDB API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.post("/upload-excel/", response_model=ProcessingResult)
async def upload_excel(file: UploadFile):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="File must be an Excel file (.xlsx)")

    start_time = time.time()

    try:
        # Read Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        if 'mobile' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must have a 'mobile' column")

        # Convert DataFrame to list of dictionaries
        records = df[['mobile']].to_dict('records')

        # Insert records in chunks
        chunk_size = 1000
        for i in range(0, len(records), chunk_size):
            chunk = records[i:i + chunk_size]
            await collection.insert_many(chunk, ordered=False)

        processing_time = time.time() - start_time

        return ProcessingResult(
            total_records=len(records),
            processing_time=processing_time,
            success=True,
            message=f"Successfully processed {len(records)} records in {processing_time:.2f} seconds"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phones/", response_model=List[PhoneNumber])
async def get_all_phones():
    phones = await collection.find().to_list(length=None)
    return phones


@app.get("/phones/{phone_number}", response_model=PhoneNumber)
async def get_phone(phone_number: str):
    phone = await collection.find_one({"mobile": phone_number})
    if not phone:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return phone


@app.put("/phones/{phone_number}", response_model=PhoneNumber)
async def update_phone(phone_number: str, phone_update: PhoneNumberUpdate):
    result = await collection.update_one(
        {"mobile": phone_number},
        {"$set": phone_update.dict(exclude_unset=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return await collection.find_one({"mobile": phone_update.mobile or phone_number})


@app.delete("/phones/{phone_number}")
async def delete_phone(phone_number: str):
    result = await collection.delete_one({"mobile": phone_number})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return {"message": "Phone number deleted successfully"}