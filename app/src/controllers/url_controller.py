from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from src.services.url_service import UrlService
from src.models import url_models
from src.database.dynamodb_client import DynamoDBClient
from src.utils.settings import settings
import logging


router = APIRouter()
logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# db_client = DynamoDBClient(settings.DYNAMODB_TABLE_NAME)
# url_service = UrlService(db_client)

def get_dynamodb_client() -> DynamoDBClient:
      return DynamoDBClient(settings.DYNAMODB_TABLE_NAME)
      

def get_url_instance(dynamodb_client: DynamoDBClient = Depends(get_dynamodb_client)) -> UrlService:
        return UrlService(dynamodb_client) 

@router.get("/health")
def health_check():
      
      logger.info("Health check endpoint called.")
      return {"status": "ok"}

@router.post("/create", response_model=url_models.CreateUrlResponse)
def create_tiny_url(payload: url_models.CreateUrlRequest, urlservice: UrlService = Depends(get_url_instance)):
    
    logger.info(f"Received request to shorten URL: {payload.original_url}")

    short_code = urlservice.create_short_url(payload.original_url, payload.phone_number)
    if not short_code:
          logger.error("Failed to create short URL.")
          raise HTTPException(status_code=500, detail="Failed to create short URL.")
    
    logger.info(f"Short URL created successfully: {short_code}")
    return url_models.CreateUrlResponse(short_code)

#           return "falied to create short_url" #need to raise http exception with status code 500
#     return url_models.CreateUrlResponse(short_code)

    