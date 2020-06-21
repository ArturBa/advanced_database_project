import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker

from modules.database.engine import engine
from modules.database.model import *


def display_all_coronadata_singleplot(session, countries):
    try:
        for country in countries:
            x = []
            confirmed = []
            deaths = []
            recovered = []
            result = session.query(Countries).filter_by(name=country).first()
            for data in result.corona_virus:
                x.append(data.date.date)
                confirmed.append(data.confirmed)
                deaths.append(data.deaths)
                recovered.append(data.recovered)
            plt.figure()
            plt.plot(x, confirmed, x, deaths, x, recovered)
            plt.title(country)
            plt.legend(['Confirmed', 'Deaths', 'Recovered'])
            plt.xlabel('Date')
            plt.ylabel('No of people')
            plt.gcf().autofmt_xdate()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    display_all_coronadata_singleplot(session, ['Poland', 'Peru'])
    plt.show()
