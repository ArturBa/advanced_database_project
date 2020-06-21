import sys
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from modules.database.engine import engine
from modules.database.model import *

def print_countries_with_death_rate(session, rate = 0.1):
    try:
        countries_list = []
        countries = session.query(Countries).all()
        for country in countries:
            if country != None:
                if len(country.corona_virus) > 0:
                    last_record = country.corona_virus[-1]
                    if last_record.deaths / last_record.confirmed > rate:
                        countries_list.append(country)
            else:
                continue
        return countries_list
    except Exception as e:
        print(e)
        
