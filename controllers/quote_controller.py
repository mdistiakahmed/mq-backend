import os
import uuid
import boto3

from fastapi import HTTPException, UploadFile

from db.dto.quote_dto import QuoteResponse, QuoteDTO
from db.repository.author_repository import AuthorRepository
from db.repository.category_repository import CategoryRepository
from db.repository.quote_repository import QuoteRepository

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)


def create_quote(category: str, author: str, image_file: UploadFile):
    try:
        random_filename = str(uuid.uuid4()) + "." + image_file.filename.split(".")[-1]
        s3.upload_fileobj(image_file.file, S3_BUCKET_NAME, random_filename)
        public_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{random_filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Could not upload image to s3"})

    quote_repository = QuoteRepository()
    result = quote_repository.create_quote(category, author, public_url)

    return 200, result


def load_paginated_quote(category: str, skip: int, limit: int) -> QuoteResponse:
    quote_repository = QuoteRepository()
    if category:
        quotes, total_items = quote_repository.get_quote_by_category(category, skip, limit)
    else:
        quotes, total_items = quote_repository.get_quote(skip, limit)

    quote_dtos = [QuoteDTO(
        quote_id=str(quote.quote_id),
        author=quote.author,
        category=quote.category,
        image_url=quote.image_url,
        like_count=quote.like_count,
        share_count=quote.share_count
    ) for quote in quotes]

    quote_response = QuoteResponse(quotes=quote_dtos, total_items=total_items)
    return quote_response


def load_quote_details(quote_id: str) -> QuoteDTO:
    quote_repository = QuoteRepository()
    quote = quote_repository.get_quote_details(quote_id)

    quote_dto = QuoteDTO(
        quote_id=str(quote.quote_id),
        author=quote.author,
        category=quote.category,
        image_url=quote.image_url,
        like_count=quote.like_count,
        share_count=quote.share_count
    )

    return quote_dto


def load_all_category():
    category_repository = CategoryRepository()
    result = category_repository.get_all_category()
    return 200, result


def create_category(name: str):
    try:
        category_repository = CategoryRepository()
        result = category_repository.create_category(name)
        return 200, result
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})


def load_all_author():
    author_repository = AuthorRepository()
    result = author_repository.get_all_author()
    return 200, result


def create_author(name: str):
    try:
        author_repository = AuthorRepository()
        result = author_repository.create_author(name)
        return 200, result
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})


