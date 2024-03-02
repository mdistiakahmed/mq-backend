from typing import List, Optional
from pydantic import BaseModel


class QuoteDTO(BaseModel):
    quote_id: str
    author: str
    category: str
    image_url: str
    like_count: int
    share_count: int


class QuoteResponse(BaseModel):
    quotes: List[QuoteDTO]
    total_items: int
