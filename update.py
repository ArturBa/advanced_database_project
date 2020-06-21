from sqlalchemy.orm import sessionmaker

from modules.database.engine import engine
from modules.update.update_air_pollution_data import update_air_pollution_data
from modules.update.air_pollution_data_preparation import prepare_air_pollution_data
from modules.update.update_corona_data import update_corona_data

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    update_corona_data(session)
    prepare_air_pollution_data()
    update_air_pollution_data(session)
