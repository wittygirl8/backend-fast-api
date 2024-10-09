from pydantic import BaseModel
from typing import Optional
from enum import Enum
from typing import Optional

# Enum for sentiment
class Sentiment(str, Enum):
    neg = "negative"
    neutral = "neutral"
    positive = "positive"

# # This schema is used for request validation and response formatting
# class ItemSchema(BaseModel):
#     id: int
#     name: str
#     description: Optional[str] = None

#     class Config:
#         orm_mode = True
    
class LinkExtractionRequest(BaseModel):
    name: str
    country: str
    domain: str
    start_year: int
    end_year: int
    sentiment: Sentiment
    number_of_urls: int = 150  # Default value

class Item(BaseModel):
    name: str
    country: str
    domain: str
    start_date: str
    end_date: str
    sentiment: Sentiment
    number_of_urls: int = 150  # Default value
