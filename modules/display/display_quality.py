import matplotlib.pyplot as plt
from modules.database.engine import engine
from sqlalchemy.orm import sessionmaker

from modules.database.engine import engine
from modules.database.model import *


def display_average_air_quality(session, country_list):
    try:
        for country in country_list:
            result = session.query(Countries).filter_by(name=country).first()
            for city in result.cities:
                no2 = []
                so2 = []
                o3 = []
                pm25 = []
                pm10 = []
                x = []
                y = []
                for quality, data in zip(city.air_quality, result.corona_virus):
                    x.append(data.date.date)
                    y.append(data.confirmed)
                    no2.append(quality.no2)
                    so2.append(quality.so2)
                    o3.append(quality.o3)
                    pm25.append(quality.pm25)
                    pm10.append(quality.pm10)
                fig, (ax1, ax2) = plt.subplots(1, 2)
                fig.suptitle('Air pollution and Coronavirus cases corellation for {}'.format(city))
                ax1.plot(x, no2, x, so2, x, o3, x, pm25, x, pm10)
                ax1.legend(['no2', 'so2', 'o3', 'pm25', 'pm10'])
                ax2.plot(x, y)
                ax1.set_xlabel('Date')
                ax2.set_xlabel('Date')
                plt.gcf().autofmt_xdate()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    display_average_air_quality(session, ['Poland'])
    plt.show()
