import urllib.request, json 
from datetime import datetime
from engine import engine
from model import CoronaVirus, Country, Dates
from sqlalchemy.orm import sessionmaker


## Do not use. Not adopted to new model design

Session = sessionmaker(bind=engine)
 session = Session()

# get json data about coronavirus in counties
with urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json") as url:
    corona_data = json.loads(url.read().decode())
    for country, country_data in corona_data.items():
        for day_data in country_data:
            record = CoronaVirus(
                            country=country, 
                            date=datetime.strptime(day_data['date'], '%Y-%m-%d'),
                            confirmed=day_data['confirmed'],
                            deaths=day_data['deaths'],
                            recovered=day_data['recovered'])
            session.add(record)
        print(f'{country} added')
session.commit()
