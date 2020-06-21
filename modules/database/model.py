from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship

from modules.database.base import Base


class Dates(Base):
    __tablename__ = 'dates'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    air_quality = relationship("AirQuality", backref="date")
    corona_virus = relationship("CoronaVirus", backref="date")

    def __repr__(self):
        return f"<Date: {self.date}>"


class Countries(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    code = Column(String(4))
    corona_virus = relationship("CoronaVirus", backref="country")
    cities = relationship("Cities", backref="country")

    def __repr__(self):
        return f"<Country: {self.name}>"


class Cities(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    air_quality = relationship("AirQuality", backref="city")
    country_id = Column(Integer, ForeignKey('countries.id'))
    name = Column(String(128))

    def __repr__(self):
        return f"<City: {self.name}>"


class CoronaVirus(Base):
    __tablename__ = 'coronavirus'
    id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey('dates.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)

    def __repr__(self):
        return f"<Corona: {self.country} {self.date} C: {self.confirmed}" \
               f" D: {self.deaths} R: {self.recovered}>"


class AirQuality(Base):
    __tablename__ = 'air_quality'
    id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey('dates.id'))
    city_id = Column(Integer, ForeignKey('cities.id'))
    so2 = Column(Float)
    no2 = Column(Float)
    o3 = Column(Float)
    pm25 = Column(Float)
    pm10 = Column(Float)

    def __repr__(self):
        return f"<Air Quality:>"
