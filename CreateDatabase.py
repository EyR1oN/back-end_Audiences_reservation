import sqlalchemy.schema
from sqlalchemy import create_engine
from sqlalchemy_utils import *

engine = create_engine("mysql+pymysql://root:qwerty@127.0.0.1/pp")

if database_exists(engine.url):
    drop_database(engine.url)

if not database_exists(engine.url):
    create_database(engine.url)
