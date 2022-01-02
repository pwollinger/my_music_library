import re
import time
import sqlite3
import requests
import configparser
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

class Album(BaseModel):
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

app = FastAPI()
CONFIGS = configparser.ConfigParser()
CONFIGS.read('config.ini')

@app.get("/discogs/")
def get_album_info(barcode: str = '', catalog: str = '', country: str = ''):
    url = f"https://api.discogs.com/database/search?barcode={barcode}&catno={catalog}&country={country}"
    header = {"Authorization": f"Discogs token={CONFIGS['Credentials']['Token']}"}

    response = requests.request("GET", url, headers=header).json().get('results')[0]

    album = {
          'id': int(time.time()/2)
        , 'title': response.get('title')
        , 'album': re.search(r'[^-]*$', response.get('title')).group().strip()
        , 'artist': re.search(r'^[^-]+', response.get('title')).group().strip()
        , 'year': response.get('year')
        , 'country': response.get('country')
        , 'catalog_number': response.get('catno')
        , 'barcode' : barcode
        , 'labels': ', '.join(map(str, response.get('label')))
        , 'genre': ', '.join(map(str, response.get('genre')))
        , 'sub_genre': ', '.join(map(str, response.get('style')))
        , 'format': response.get('formats')[0].get('name')
        , 'cover_url': response.get('cover_image')
    } 

    return album

@app.post("/album/")
def create_album(album: Album):
    con = sqlite3.connect(CONFIGS['Database']['db_file'])
    cur = con.cursor()

    query = f"INSERT INTO {CONFIGS['Database']['table']} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cur.executemany(query, tuple(list(album.values())))
    con.commit()

    con.close()

    return album.get(id)