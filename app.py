import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

# Importa tu función para clasificar el tono de piel
from api.model import classify_skin_tone  

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Endpoint principal
@app.get("/")
async def root():
    return {"message": "Hello, welcome to the skin tone classification API!"}

# Endpoint para verificar el estado del servicio
@app.get("/check")
async def check():
    return {"status": "API is running"}

# Endpoint para clasificar el tono de piel a partir de una imagen
@app.post("/classify-skin-tone/")
async def classify_skin_tone_endpoint(file: UploadFile = File(...)):
    logger.info(f"Received request to classify skin tone for file: {file.filename}")
    
    try:
        # Leer el archivo de imagen
        image_data = await file.read()

        # Usar la función classify_skin_tone para procesar la imagen
        skin_tone_category = classify_skin_tone(image_data)
        
        logger.info(f"Skin tone classified for {file.filename}: {skin_tone_category}")
        return JSONResponse(content={"skin_tone": skin_tone_category})
    
    except ValueError as e:
        logger.error(f"File format error for {file.filename}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error processing the image {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error processing the image")
