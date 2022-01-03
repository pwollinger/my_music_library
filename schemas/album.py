from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AlbumSchema(BaseModel):
    id: int
    title: str
    album: str
    artist: str
    year: Optional[int]
    country: str
    catalog_number: str
    barcode: Optional[str]
    labels: Optional[str]
    genre: Optional[str]
    sub_genre: Optional[str]
    format: Optional[str]
    cover_url: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True