from modules.database.model import *


def get_countries_with_more(session, country, date, search_type='confirmed'):
    """
    Get countries with more cases than a selected country
    >>> get_countries_with_more(session, 'Italy', '2020-03-07')
    ['China', 'Korea, South']

    @param session: database session
    @param country: selected country to compare to
    @param date: day of comparision
    @param search_type: type of comparision: ['confirmed', 'deaths', 'recovered']

    @return countries: Array of countries meeting the comparision
    """
    try:
        counties_id = []
        country_data = session.query(Countries).filter_by(name=country).first()
        date = session.query(Dates).filter_by(date=date).first()
        cases = session.query(CoronaVirus).filter(CoronaVirus.country_id == country_data.id,
                                                  CoronaVirus.date_id == date.id).first()
        if search_type == 'confirmed':
            counties_id = session.query(CoronaVirus.country_id).filter(CoronaVirus.confirmed > cases.confirmed,
                                                                       CoronaVirus.date_id == date.id).all()
        elif search_type == 'deaths':
            counties_id = session.query(CoronaVirus.country_id).filter(CoronaVirus.deaths > cases.deaths,
                                                                       CoronaVirus.date_id == date.id).all()
        elif search_type == 'recovered':
            counties_id = session.query(CoronaVirus.country_id).filter(CoronaVirus.recovered > cases.recovered,
                                                                       CoronaVirus.date_id == date.id).all()
        else:
            print('wrong search type')
            return None
        counties_id = [country_id[0] for country_id in counties_id]
        counties = session.query(Countries.name).filter(Countries.id.in_(counties_id)).all()
        counties = [country[0] for country in counties]
        return counties

    except Exception as e:
        print(e)
        return None
