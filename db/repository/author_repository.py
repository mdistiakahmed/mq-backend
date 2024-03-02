import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import func

from config.config_manager import CONFIG
from db import DB_PATH
from db.db_connector import DbConnector
from db.entities.author_model import AuthorTable


class AuthorRepository:
    def __init__(self):
        self.db_connector = DbConnector(DB_PATH, CONFIG.db_schema)
        logging.info(f"Database connector initialized {self.db_connector}")

    def create_author(self, name: str) -> dict:
        lower_name = name.lower()
        new_author = AuthorTable(
            name=lower_name
        )
        try:
            self.db_connector.connect()
            existing_category = self.db_connector.session.query(AuthorTable).filter(
                func.lower(AuthorTable.name) == lower_name).first()
            if existing_category:
                logging.error("Author with similar name already exists")
                raise ValueError("Author with similar name already exists")

            self.db_connector.session.add(new_author)
            self.db_connector.session.commit()

            return new_author
        except Exception as e:
            print(f"Error while saving author to db: {e}")
            raise HTTPException(status_code=500, detail=e)
        finally:
            self.db_connector.disconnect()

    def get_all_author(self) -> List[str]:
        try:
            self.db_connector.connect()
            authors = self.db_connector.session.query(AuthorTable).all()
            author_names = [author.name for author in authors]

            return author_names
        except Exception as e:
            print(f"Error while loading author from db: {e}")
        finally:
            self.db_connector.disconnect()
