import pandas as pd
import plotly.express as px
import pycountry

from modules.database.model import *


def get_dataframe(session):
    dataframe = pd.read_sql(
        session.query(Countries, CoronaVirus, Dates).filter(Countries.id == CoronaVirus.country_id).filter(
            CoronaVirus.date_id == Dates.id).statement, session.bind)
    del dataframe['id']
    del dataframe['country_id']
    del dataframe['date_id']
    dataframe = dataframe.rename(columns={'name': 'country'})

    d_country_code = {}  # To hold the country names and their ISO
    for country in dataframe['country'].unique():
        try:
            country_data = pycountry.countries.search_fuzzy(country)
            # country_data is a list of objects of class pycountry.db.Country
            # The first item  ie at index 0 of list is best fit
            # object of class Country have an alpha_3 attribute
            country_code = country_data[0].alpha_3
            d_country_code.update({country: country_code})
        except:
            print('could not add ISO 3 code for ->', country)
            # If could not find country, make ISO code ' '
            d_country_code.update({country: ' '})

    # create a new column iso_alpha in the df
    # and fill it with appropriate iso 3 code
    for k, v in d_country_code.items():
        dataframe.loc[(dataframe.country == k), 'iso_alpha'] = v

    dataframe.date = pd.to_datetime(dataframe.date)
    dataframe['date'] = dataframe['date'].dt.strftime('%Y-%m-%d')
    return dataframe


def display_map_confirmed(session):
    dataframe = get_dataframe(session)
    fig = px.choropleth(data_frame=dataframe,
                        locations="iso_alpha",
                        color="confirmed",  # value in column 'Confirmed' determines color
                        hover_name="country",
                        color_continuous_scale='deep',  # color scale
                        animation_frame="date")
    fig.update_layout(
        title_text='Global confirmed cases of Coronavirus',
        title_x=0.5
    )
    fig.show()


def display_map_deaths(session):
    dataframe = get_dataframe(session)
    fig = px.choropleth(data_frame=dataframe,
                        locations="iso_alpha",
                        color="deaths",  # value in column 'death' determines color
                        hover_name="country",
                        color_continuous_scale='deep',  # color scale
                        animation_frame="date")
    fig.update_layout(
        title_text='Global death cases of Coronavirus',
        title_x=0.5
    )
    fig.show()


def display_map_recovered(session):
    dataframe = get_dataframe(session)
    fig = px.choropleth(data_frame=dataframe,
                        locations="iso_alpha",
                        color="recovered",  # value in column 'recovered' determines color
                        hover_name="country",
                        color_continuous_scale='deep',  # color scale
                        animation_frame="date")
    fig.update_layout(
        title_text='Global recovered cases of Coronavirus',
        title_x=0.5
    )
    fig.show()
