import configs.config as CONFIGS
from configs.database import Base
from sqlalchemy import Column, DateTime, Integer, String

class Album(Base):
    __tablename__ = CONFIGS.get_table()
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    album = Column(String(256), nullable=False)
    artist = Column(String(256), nullable=False)
    year = Column(Integer, nullable=False)
    country = Column(String(256), nullable=False)
    catalog_number = Column(String(256), nullable=False)
    barcode = Column(String(256))
    labels = Column(String(256))
    genre = Column(String(256))
    sub_genre = Column(String(256))
    format = Column(String(256))
    cover_url = Column(String(256))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)