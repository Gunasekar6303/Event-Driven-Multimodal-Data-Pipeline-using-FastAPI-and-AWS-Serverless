from fastapi import FastAPI, UploadFile, File
import boto3
import uuid

app = FastAPI()

BUCKET_NAME = "your s3 bucket name"

s3 = boto3.client("s3")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    key = f"uploads/{file_id}_{file.filename}"

    contents = await file.read()

    s3.put_object(
        Bucket = BUCKET_NAME,
        Key = key,
        Body = contents
    )

    return{
        "filename": key,
        "message": "File uploaded successfully"
    }
