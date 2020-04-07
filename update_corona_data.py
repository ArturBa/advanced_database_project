import urllib.request, json 
from datetime import date, datetime
from sqlalchemy.orm import sessionmaker
from engine import engine
from model import CoronaVirus, Countries, Dates
from utils import get_or_create


# Start a session
Session = sessionmaker(bind=engine)
session = Session()

# Get last update date from db
last_day_db = session.query(Dates).all()
if last_day_db: 
    last_day_db = last_day_db[-1].date
else: 
    last_day_db = date.fromordinal(1)

# get json data about coronavirus in counties
with urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json") as url:
    corona_data = json.loads(url.read().decode())
    for country, country_data in corona_data.items():
        contry_db = get_or_create(session, Countries, name=country)

        for day in country_data:
            day_date = datetime.strptime(day['date'], '%Y-%m-%d').date()

            # Check the current date with last in db
            if (last_day_db < day_date):
                # If the json date is newer add to db

                day_db = get_or_create(session, Dates, date=day_date)


                record = CoronaVirus(
                            country=contry_db, 
                            date=day_db,
                            confirmed=day['confirmed'],
                            deaths=day['deaths'],
                            recovered=day['recovered'])
                session.add(record)
        session.commit()
        print(f'{country} added')
