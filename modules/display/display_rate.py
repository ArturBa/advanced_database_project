from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from engine import engine
from model import *
import numpy as np

def display_all_coronadata_singleplot(session, countries):
    try:
        for country in countries:
            x = []
            confirmed = []
            rate = np.array([])
            result = session.query(Countries).filter_by(name=country).first()
            for data in result.corona_virus:
                x.append(data.date.date)
                confirmed.append(data.confirmed)
            rate = np.diff(confirmed)
            plt.figure()
            plt.plot(x[1:], rate)
            plt.title('Coronavirus confirmed cases rate for: ' + country)
            plt.legend(['Confirmed rate'])
            plt.xlabel('Date')
            plt.gcf().autofmt_xdate()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    display_all_coronadata_singleplot(session, ['Poland', 'Peru'])
    plt.show()
