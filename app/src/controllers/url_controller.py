from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from src.services.url_service import UrlService
from src.models.url_models import CreateUrlRequest, CreateUrlResponse
from src.database.dynamodb_client import DynamoDBClient
from src.utils.settings import settings
import logging


router = APIRouter()
logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# db_client = DynamoDBClient(settings.dynamodb_table_name)
# url_service = UrlService(db_client) 


@router.get("/health")
def health_check():
      
      logger.info("Health check endpoint called.")
      return {"status": "ok"}

# @router.post("/create", response_model=CreateUrlResponse)
# def create_tiny_url(payload: CreateUrlRequest):
    
#     logger.info(f"Received request to shorten URL: {payload.original_url}")

#     short_code = UrlService.create_short_url(payload.original_url, payload.phone_number)

#     if not short_code:
#         logger.error("Failed to create short URL.")
#         raise HTTPException(status_code=500, detail="Failed to create short URL.")

#     short_url = f"https://tinyurl.com/{short_code}"
#     logger.info(f"Short URL created successfully: {short_url}")

#     return CreateUrlResponse(short_url=short_url)
  