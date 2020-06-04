import sys
sys.path.append('../..')
sys.path.append('../database/')
sys.path.append('../display/')
sys.path.append('../update/')
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from modules.database.engine import engine
from modules.database.model import *

def print_countries_with_recovered_rate(session, rate = 0.5):
    try:
        countries_list = []
        countries = session.query(Countries).all()
        print("countries = ", countries)
        for country in countries:
            if country != None:
                if len(country.corona_virus) > 0:
                    last_record = country.corona_virus[-1]
                    if last_record.recovered / last_record.confirmed > rate:
                        countries_list.append(country)
            else:
                continue
        return countries_list
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    print("Result = ", print_countries_with_recovered_rate(session))
