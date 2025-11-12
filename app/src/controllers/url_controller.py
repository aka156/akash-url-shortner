from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, HttpUrl
from src.services.url_service import UrlService
from src.models import url_models
from src.database.dynamodb_client import DynamoDBClient
from src.utils.settings import settings
from fastapi.responses import RedirectResponse
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
def create_tiny_url( request: Request,payload: url_models.CreateUrlRequest, urlservice: UrlService = Depends(get_url_instance)): #request should be the first parameter
    
    logger.info(f"Received request to shorten URL: {payload.original_url}")

    short_code = urlservice.create_short_url(payload.original_url, payload.phone_number)
    if not short_code:
          logger.error("Failed to create short URL.")
          raise HTTPException(status_code=500, detail="Failed to create short URL.")
    
    logger.info(f"Short URL created successfully: {short_code}")
    base_url = str(request.base_url)
    short_url = f"{base_url}{short_code}"

    logger.info(f"Created new mapping: {short_url} for phone: {payload.phone_number}")
    return url_models.CreateUrlResponse(short_url=short_url) #parameters should be given in key value pairs
            # "short_url": "http://127.0.0.1:8000/2ygsejy8" :- this is short url after we hit the endpoint

#     return "falied to create short_url" #need to raise http exception with status code 500
#     return url_models.CreateUrlResponse(short_code)

@router.get("/{short_code}")
def get_short_code(request: Request,short_code:str,url_service: UrlService = Depends(get_url_instance)):
      original_url = url_service.get_original_url(short_code)
      if not original_url:
         logger.error("Failed to find original url.")
         raise HTTPException(status_code=404, detail="URL not found.")
      return RedirectResponse(url=original_url, status_code=307)

@router.get("/fetch/{short_code}")
def fetch_short_code(request: Request,short_code:str,url_service: UrlService = Depends(get_url_instance)):
      #logger.info(f"short_code :{short_code}")
      # short_code = short_code.strip("{}")
      original_url = url_service.get_original_url(short_code)


      if not original_url:
           logger.error("failed to find original url")
           raise HTTPException(status_code=404,detail="url not found")
      return url_models.FetchUrlResponse(original_url=original_url) #return with models
      # return {"original_url": original_url} #return without models

@router.delete("/delete/{short_code}")
def delete_short_code(request: Request,short_code:str, url_service: UrlService = Depends(get_url_instance)):
#      short_code = short_code.strip("{}")
     status = url_service.delete_short_url(short_code) # we are calling delete_short_url function from url_service by passing short_code as input
     if not status:
          logger.error("failed to delete short url")
          raise HTTPException(status_code = 404,detail="URL not found")
     return {"message":"URL deleted successfully"}