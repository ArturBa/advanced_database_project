import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker

from modules.database.engine import engine
from modules.database.model import *


def display_confirmed(session, country_name):
    try:
        for country in country_name:
            country_data = session.query(Countries).filter_by(name=country).first()
            x = []
            y = []
            for data in country_data.corona_virus:
                x.append(data.date.date)
                y.append(data.confirmed)
            plt.plot(x, y)
        plt.legend(country_name)
        plt.title(f'Confirmed cases')
        plt.xlabel('Date')
        plt.ylabel('Confirmed cases')
        plt.gcf().autofmt_xdate()

    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    display_confirmed(session, ['Peru', 'Poland'])
    plt.show()
