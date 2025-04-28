from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

app = FastAPI()


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Megabytes in bytes

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Check if a file was actually uploaded
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file uploaded. Please upload a valid file."
            )

        # Read the file contents
        contents = await file.read()

        # Check if the uploaded file is empty
        if len(contents) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )

        # Check if the file size exceeds the maximum allowed size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE // (1024*1024)}MB."
            )

        # If all checks pass, return a success response
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "File uploaded successfully!",
                "filename": file.filename,
                "size_in_bytes": len(contents)
            }
        )

    except Exception as e:
        # Handle any unexpected errors gracefully
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while uploading the file: {str(e)}"
        )

