import csv
from datetime import date, datetime, timedelta
from sqlalchemy.orm import sessionmaker
from engine import engine
from model import AirQuality, Countries, Dates, Cities
from utils import get_or_create


# Start a session
Session = sessionmaker(bind=engine)
session = Session()

# Get last update date from db
dates = session.query(Dates).all()
dates_air_quality = list(filter(lambda date: date.air_quality != [], dates))
if dates_air_quality:
    first_no_air_quality_day = dates_air_quality[-1].date + timedelta(days=1)
else: 
    first_no_air_quality_day = date.fromordinal(1)
print(first_no_air_quality_day)
exit(0)


def get_or_create_city(session, name, country_code):
    instance = session.query(Cities).filter_by(name=name).first()
    if instance:
        return instance
    else:
        country = get_or_create(session, Countries, code=country_code)
        instance = Cities(name=name, country=country)
        session.add(instance)
        session.commit()
        return instance


with open('AirPollutionFinal.csv', 'r') as air_pollution_csv:
    csv_reader = csv.reader(air_pollution_csv)
    header = True
    for row in csv_reader:
        if header:
            header = False
            continue
        date = datetime.strptime(row[1], '%Y-%m-%d').date()
        if first_no_air_quality_day < date:
            city = get_or_create_city(session, row[0], row[2])
            date_db = get_or_create(session, Dates, date=date)

            air_pollution = AirQuality(
                    date=date_db, city=city, so2=row[7], no2=row[3], 
                    o3=row[4], pm25=row[6], pm10=row[5]
                    )
            session.add(air_pollution)
            session.commit()
            print(f'Added data for {row[0]} from day: {row[1]}')

