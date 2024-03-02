from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DbConnector:

    def __init__(self, db_url: str, db_schema: str):
        self.session = None
        self.engine = create_engine(
            db_url, connect_args={"options": "-csearch_path={}".format(db_schema)}
        )
        self.Session = sessionmaker(bind=self.engine)

    def connect(self):
        self.session = self.Session()

    def disconnect(self):
        self.session.close()

    def execute_query(self, query):
        self.connect()
        result = self.session.execute(query)
        self.disconnect()
        return result
