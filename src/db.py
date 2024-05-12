from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import sessionmaker

from src.schema import Base
from src.singleton import Singleton

class Database(metaclass=Singleton):
    def __init__(self, db_url):
        self.engine = create_engine(db_url)

        Base.metadata.create_all(self.engine)

        self.session = sessionmaker(bind=self.engine)()
        self.__initialized = True

    def close(self):
        self.session.close()
        self.engine.dispose()
        self.__initialized = False

db = Database("postgresql://username:password@localhost/database_name")
session = db.session
