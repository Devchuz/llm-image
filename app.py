import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from api.model import classify_skin_tone

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()



@app.post("/classify-skin-tone/")
async def classify_skin_tone_endpoint(file: UploadFile = File(...)):

    logger.info(f"Received request to classify skin tone for file: {file.filename}")
    
    try:
        # Use the classify_skin_tone function to process the image
        skin_tone_category = classify_skin_tone(file)
        logger.info(f"Skin tone classified for {file.filename}: {skin_tone_category}")
        return JSONResponse(content={"skin_tone": skin_tone_category})
    except ValueError as e:
        logger.error(f"File format error for {file.filename}: {e}")
        # Handle unsupported file format error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing the image {file.filename}: {e}")
        # Handle any other unexpected errors
        raise HTTPException(status_code=500, detail="Error processing the image")
