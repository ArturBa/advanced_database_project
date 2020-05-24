import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker

from modules.database.engine import engine
from modules.database.model import *


def dict_upsert(dictionary, key, value, number):
    try:
        dictionary.update({key: dictionary[key] + value / number})
        return dictionary
    except KeyError:
        dictionary.update({key: value})
        return dictionary


def display_average_air_quality(session, country_list):
    try:
        for country in country_list:
            result = session.query(Countries).filter_by(name=country).first()
            no2_dict = {}
            so2_dict = {}
            o3_dict = {}
            pm25_dict = {}
            pm10_dict = {}
            cities_no = len(result.cities)
            for city in result.cities:
                x = []
                y = []
                for quality, data in zip(city.air_quality, result.corona_virus):
                    x.append(data.date.date)
                    y.append(data.confirmed)
                    no2_dict = dict_upsert(no2_dict, data.date.date, quality.no2, cities_no)
                    so2_dict = dict_upsert(so2_dict, data.date.date, quality.so2, cities_no)
                    o3_dict = dict_upsert(o3_dict, data.date.date, quality.o3, cities_no)
                    pm25_dict = dict_upsert(pm25_dict, data.date.date, quality.pm25, cities_no)
                    pm10_dict = dict_upsert(pm10_dict, data.date.date, quality.pm10, cities_no)
            length = len(x)
            if len(x) > len(no2_dict):
                length = len(no2_dict)
            elif len(no2_dict)>len(x):
                length = len(x)
            else:
                pass
            fig, (ax1,ax2) = plt.subplots(1,2)
            fig.suptitle('Average air pollution coefficients and coronavirus confirmed cases corellation for {}'.format(country))
            ax1.plot(x,list(no2_dict.values())[:length], x,list(so2_dict.values())[:length], x,list(o3_dict.values())[:length], x,list(pm25_dict.values())[:length], x,list(pm10_dict.values())[:length])
            ax1.legend(['no2', 'so2', 'o3', 'pm25', 'pm10'])
            ax2.plot(x, y)
            ax2.legend(['Confirmed cases'])
            ax1.set_xlabel('Date')
            ax2.set_xlabel('Date')
            plt.gcf().autofmt_xdate()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    display_average_air_quality(session, ['Italy', 'Spain'])
    plt.show()
