import sys
sys.path.append('../..')
sys.path.append('../database/')
sys.path.append('../display/')
sys.path.append('../update/')

from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from modules.database.engine import engine
from modules.database.model import *
import numpy as np
from scipy.interpolate import UnivariateSpline
from math import ceil


def test(x,a,b):
    return a* np.exp(b*x)

def display_rate(session, countries):
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
            x_vals = np.linspace(0, len(rate), int(len(rate) / 10) + 1)
            s = UnivariateSpline(x_vals, rate[::10])
            xnew = np.linspace(0, len(rate), len(rate))
            ynew = s(xnew)
            plt.figure()
            plt.plot(x[1:], rate, 'o', x[1:], ynew)
            plt.title('Coronavirus confirmed cases rate for: ' + country)
            plt.legend(['Confirmed rate', 'Confirmed rate interpolated'])
            plt.xlabel('Date')
            plt.gcf().autofmt_xdate()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    display_rate(session, ['Poland', 'Peru', 'Japan'])
    plt.show()
