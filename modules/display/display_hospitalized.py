from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from modules.database.engine import engine
from modules.database.model import *


def display_hospitalized(session, countries):
    try:
        for country in countries:
            x = []
            hospitalized = []
            result = session.query(Countries).filter_by(name=country).first()
            for data in result.corona_virus:
                x.append(data.date.date)
                hospitalized.append(data.confirmed - data.deaths - data.recovered)
            plt.figure()
            plt.plot(x, hospitalized)
            plt.title('No of people being hospitalized in: ' + country)
            plt.legend(['Hospitalized'])
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
