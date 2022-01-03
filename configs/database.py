import configparser
from configs.config import CONFIGS
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

CONFIGS = configparser.ConfigParser()
CONFIGS.read('configs/config.ini')

engine = create_engine(f"sqlite:///database.db")
Base = declarative_base()
LocalSession = sessionmaker(bind=engine, expire_on_commit=False)