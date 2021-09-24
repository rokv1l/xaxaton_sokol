from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

import config

base = declarative_base()


data = {
    'drivername': 'postgresql',
    'host': config.db_host,
    'port': config.db_port,
    'username': config.db_username,
    'password': config.db_password,
    'database': config.db_name,
}

while True:
    try:
        engine = create_engine(URL(**data))
        session_maker = sessionmaker(bind=engine)
        break
    except OperationalError as e:
        print(e)
        print('Cant connect to database. Try again...')
        sleep(5)
