import os

from sqlalchemy import create_engine

from modules.database.base import Base

# get dabase uri
db_string = os.getenv('DB_URI')

# create database engine
engine = create_engine(db_string)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
