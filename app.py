import os
from sqlalchemy import create_engine
from base import Base
from model import CoronaVirus

db_string = os.getenv('DB_URI')

engine = create_engine(db_string)
str(Base.metadata.create_all(engine))

