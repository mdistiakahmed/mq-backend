import os
from fastapi import APIRouter, HTTPException, UploadFile, Form, Query
from pydantic import BaseModel

from controllers.quote_controller import create_quote, load_all_category, create_category, load_all_author, \
    create_author, load_paginated_quote, load_quote_details
from db.dto.quote_dto import QuoteResponse

ORIGINAL_SECRET_VALUE = os.environ.get('UPLOAD_SECRET')


router = APIRouter()


@router.post("/quote-upload")
async def upload_image(category: str = Form(...), author: str = Form(...),
                       secret: str = Form(...), image_file: UploadFile = Form(...)):
    # Validate secret
    if secret != ORIGINAL_SECRET_VALUE:
        raise HTTPException(status_code=403, detail="Secret value is incorrect")

    # Validate image file type
    allowed_image_types = ['image/png', 'image/jpg', 'image/jpeg']
    if image_file.content_type not in allowed_image_types:
        raise HTTPException(status_code=422, detail="Only PNG, JPG, or JPEG files allowed")

    # Validate image file size
    max_image_size_kb = 300
    if image_file.size > max_image_size_kb * 1024:
        raise HTTPException(status_code=422, detail="Image size exceeds 300KB limit")

    return_code, response = create_quote(category, author, image_file)
    return response


@router.get("/quotes", response_model=QuoteResponse)
async def get_quotes(category: str = None, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    try:
        quotes = load_paginated_quote(category, skip, limit)
        return quotes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/quotes/{quote_id}")
async def get_quotes(quote_id: str):
    try:
        quote = load_quote_details(quote_id)
        return quote
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


class CategoryRequest(BaseModel):
    name: str


class AuthorRequest(BaseModel):
    name: str


@router.get("/category")
async def get_all_category():
    return_code, response = load_all_category()
    return response


@router.post("/category")
async def create_new_category(category_request: CategoryRequest):
    return_code, response = create_category(category_request.name)
    return response


@router.get("/author")
async def get_all_author():
    return_code, response = load_all_author()
    return response


@router.post("/author")
async def create_new_author(author_request: AuthorRequest):
    return_code, response = create_author(author_request.name)
    return response
