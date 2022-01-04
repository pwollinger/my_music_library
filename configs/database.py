import configparser
import configs.config as CONFIGS
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(f"sqlite:///{CONFIGS.get_database()}")
Base = declarative_base()
LocalSession = sessionmaker(bind=engine, expire_on_commit=False)