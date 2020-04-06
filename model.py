from sqlalchemy import Column, Integer, String, Date
from base import Base


class CoronaVirus(Base):
    __tablename__ = 'coronavirus'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    county = Column(String(128))
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)

    def __repl__(self):
        return f"<Corona: {self.county} {self.date} C: {self.confirmed}"\
                " D: {self.deaths} R: {self.recovered}>" 
