from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os

app = FastAPI()

os.makedirs("assets", exist_ok=True)

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):

    extensions = ["txt", "pdf"]
    filename = file.filename
    file_extension = filename.split(".")[-1].lower()

    if file_extension not in extensions:
        raise HTTPException(
            status_code=400,
            detail="Only txt and pdf files formats are accepted."
        )
    
    maxSize= 5 * 1024 * 1024 #size in bytes
    data = await file.read()
    file_size = len(data)
    if file_size > maxSize:
        raise HTTPException(
            status_code=400,
            detail="Max file size allowed is 5 MB."
        )

    file_location = f"assets/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"info": f"File '{file.filename}' saved at '{file_location}'"}