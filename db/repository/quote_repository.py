import logging

from config.config_manager import CONFIG
from db import DB_PATH
from db.db_connector import DbConnector
from db.entities.quote_models import QuoteTable
from uuid import UUID


class QuoteRepository:
    def __init__(self):
        self.db_connector = DbConnector(DB_PATH, CONFIG.db_schema)
        logging.info(f"Database connector initialized {self.db_connector}")

    def create_quote(self, category: str, author: str, image_url: str) -> dict:
        logging.info(f"Set new quote value on UserTable")

        new_quote = QuoteTable(
            author=author,
            category=category,
            image_url=image_url
        )

        try:
            self.db_connector.connect()
            result = self.db_connector.session.add(new_quote)
            result = self.db_connector.session.commit()

            return result
        except Exception as e:
            print(f"Error while saving quotes to db: {e}")
        finally:
            self.db_connector.disconnect()

    def get_quote(self, skip: int = 0, page_size: int = 10):
        try:
            self.db_connector.connect()
            quotes_query = self.db_connector.session.query(QuoteTable)
            total_items = quotes_query.count()
            quotes = quotes_query.offset(skip).limit(page_size).all()

            return quotes, total_items
        except Exception as e:
            print(f"Error while loading category from db: {e}")
        finally:
            self.db_connector.disconnect()

    def get_quote_details(self, quote_id: str):
        try:
            quote_uuid = UUID(quote_id)
            self.db_connector.connect()
            quote = self.db_connector.session.query(QuoteTable).filter(QuoteTable.quote_id == quote_uuid).one()

            return quote
        except Exception as e:
            print(f"Error while loading category from db: {e}")
        finally:
            self.db_connector.disconnect()

    def get_quote_by_category(self, category: str, skip: int = 0, page_size: int = 10):
        try:
            self.db_connector.connect()
            quotes_query = self.db_connector.session.query(QuoteTable).filter(QuoteTable.category == category)
            total_items = quotes_query.count()
            quotes = quotes_query.offset(skip).limit(page_size).all()

            return quotes, total_items
        except Exception as e:
            print(f"Error while loading category from db: {e}")
        finally:
            self.db_connector.disconnect()
