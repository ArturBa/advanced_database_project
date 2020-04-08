from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from engine import engine
from model import *

def display_confirmed(session, country_name):
    try:
        country = session.query(Countries).filter_by(name=country_name).first()
        x = []
        y = []
        for data in country.corona_virus:
            x.append(data.date.date)
            y.append(data.confirmed)
        plt.plot(x, y)
        plt.title(f'Confirmed cases in {country_name}')
        plt.xlabel('Date')
        plt.ylabel('Confirmed cases')
        plt.gcf().autofmt_xdate()

    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    display_confirmed(session, 'Peru')
    plt.show()

