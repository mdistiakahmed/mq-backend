import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import func

from config.config_manager import CONFIG
from db import DB_PATH
from db.db_connector import DbConnector
from db.entities.category_models import CategoryTable


class CategoryRepository:
    def __init__(self):
        self.db_connector = DbConnector(DB_PATH, CONFIG.db_schema)
        logging.info(f"Database connector initialized {self.db_connector}")

    def create_category(self, name: str) -> dict:
        lower_name = name.lower()
        new_category = CategoryTable(
            name=lower_name
        )
        try:
            self.db_connector.connect()
            existing_category = self.db_connector.session.query(CategoryTable).filter(
                func.lower(CategoryTable.name) == lower_name).first()
            if existing_category:
                logging.error("Category with similar name already exists")
                raise ValueError("Category with similar name already exists")

            self.db_connector.session.add(new_category)
            self.db_connector.session.commit()

            return new_category
        except Exception as e:
            print(f"Error while saving quotes to db: {e}")
            raise HTTPException(status_code=500, detail=e)
        finally:
            self.db_connector.disconnect()

    def get_all_category(self) -> List[str]:
        try:
            self.db_connector.connect()
            categories = self.db_connector.session.query(CategoryTable).all()
            category_names = [category.name for category in categories]

            return category_names
        except Exception as e:
            print(f"Error while loading category from db: {e}")
        finally:
            self.db_connector.disconnect()
