import json
import urllib.request
from datetime import date, datetime, timedelta

from sqlalchemy.orm import sessionmaker

from engine import engine
from model import CoronaVirus, Countries, Dates
from utils import get_or_create

# Start a session
Session = sessionmaker(bind=engine)
session = Session()

# Get last update date from db
dates = session.query(Dates).all()
print(dates[0])
dates_virus = list(filter(lambda date: date.corona_virus != [], dates))
if dates_virus:
    first_no_virus_day = dates_virus[-1].date + timedelta(days=1)
else:
    first_no_virus_day = date.fromordinal(1)

# get json data about coronavirus in counties
with urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json") as url:
    corona_data = json.loads(url.read().decode())
    for country, country_data in corona_data.items():
        contry_db = get_or_create(session, Countries, name=country)

        for day in country_data:
            day_date = datetime.strptime(day['date'], '%Y-%m-%d').date()

            # Check the current date with last in db
            if first_no_virus_day < day_date:
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
