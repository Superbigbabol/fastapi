import datetime
import decimal
from http.client import HTTPException
import json
from typing import Annotated
import uvicorn
from fastapi import FastAPI, APIRouter, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from bson.objectid import ObjectId

import gridfs
from uploadfiles import upload_file
from database.schemas import all_data, individual_data
from database.models import Payment
from config import collection, db
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()
router = APIRouter(prefix="/api/v1")

origins = [
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

# get_payments(...): Fetches payments with the following calculations performed server-side:
    # Method should support filter, search and paging
@router.get("/get_payments")
async def get_payments():
    # limit 10 for testing .limit(10)
    data = collection.find()
    # return all_data(data) 
    return JSONResponse(jsonable_encoder(all_data(data)), status_code=200, headers={"Content-Type": "application/json"})

@router.get("/get_payment_by_id/{id}")
async def get_payment_by_id(id:str):
    
    try:
        data = collection.find_one({"_id": ObjectId(id)})
        if not data:
            return HTTPException(status_code=404, detail=f"Payment does not exist")
        return JSONResponse(jsonable_encoder(individual_data(data)), status_code=200, headers={"Content-Type": "application/json"})
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error in get_payment_by_id {e}")
    

@router.put("/{payment_id}")
async def update_payment(payment_id:str, updated_payment:Payment):
    try:
        id = ObjectId(payment_id)
        existing_doc = collection.find_one({"_id":id})
        if not existing_doc:
            return HTTPException(status_code=404, detail=f"Payment does not exist")
        # print(dict(updated_payment))
        result = collection.update_one({"_id":id}, {"$set":dict(updated_payment)})
        return {
                "status_code":200, 
                "message":"Updated Successfully",
                "modified_count": str(result.modified_count) 
                }
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error in update_payment {e}")

# delete_payment(...): Deletes one payment by ID. Returns success or error.
@router.delete("/{payment_id}")
async def delete_payment(payment_id:str):
    try:
        id = ObjectId(payment_id)
        existing_doc = collection.find_one({"_id":id})
        if not existing_doc:
            return HTTPException(status_code=404, detail=f"Payment does not exist")
        resp = collection.delete_one({"_id":id})
        return {"status_code":200, "message":"delete Successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error in delete_payment {e}")

# create_payment(...): Creates a new payment. Returns the ID of the new record or error.
@router.post("/")
async def create_payment(new_payment: Payment):
    try:
        # maybe need to map manually
        resp = collection.insert_one(dict(new_payment))
        return {"status_code":200, "id":str(resp.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error in create_payment {e}")

# upload_evidence(...): Allows uploading evidence files (PDF, PNG, JPG) when updating status to completed.
# update_payment(...): Updates one payment.
# -----Allow users to upload evidence files (PDF, PNG, JPG) when the payment status is updated to “completed”.
# -----Payments cannot be marked as completed without uploading an evidence file.
# -----Store the evidence file in MongoDB.
# -----Generate a download link for the uploaded evidence file.
@router.post("/upload_evidence")
async def upload_evidence(evidence: UploadFile = File(...), updatedPayment: str = Form(...)):
    fs = gridfs.GridFS(db, collection="files")
    evidence_content = await evidence.read()
    payment_data = json.loads(updatedPayment)
    fid = fs.put(evidence_content, filename=evidence.filename)
    print(payment_data["id"])
    print(payment_data)
    id = ObjectId(payment_data["id"])
    # delete id mapped from json, mongodb is _id
    payment_data.pop("id")
    # add fid to existing doc
    payment_data['fid'] = str(fid)

    result = collection.update_one({"_id":id}, {"$set":payment_data})
    return {
        "payment_data": payment_data,
        "evidence_filename": evidence.filename,
        "fid": str(fid),
        "modified_count": str(result.modified_count),
        "status_code": 200,
        "message":"Updated Successfully"
    }

# download_evidence(...): Returns uploaded evidence file which should be saved from UI.
@router.get("/download/{fid}")
async def download_evidence(fid: str):
    fs = gridfs.GridFS(db, collection="files")
    id = ObjectId(fid)
    fs.get(id).read()
    return { 
        "status_code": 200,
        "message": "Download Successfully"
    }

app.include_router(router)


