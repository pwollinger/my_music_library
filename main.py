import re
import requests
import configparser
from typing import List
from datetime import datetime
from models.album import Album
import configs.config as CONFIGS
from sqlalchemy.orm import Session
from schemas.album import AlbumSchema
from configs.database import Base, engine, LocalSession
from fastapi import status, Depends, FastAPI, HTTPException

Base.metadata.create_all(engine)

app = FastAPI()

def get_session():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()

@app.get("/discogs/")
def get_album_info(barcode: str = '', catalog: str = '', country: str = ''):
    url = f"https://api.discogs.com/database/search?barcode={barcode}&catno={catalog}&country={country}"
    header = {"Authorization": f"Discogs token={CONFIGS.get_token()}"}

    response = requests.request("GET", url, headers=header).json().get('results')

    albums = []
    
    for release in response:
        album = {
            'id': release.get('id')
            , 'title': release.get('title')
            , 'album': re.search(r'[^-]*$', release.get('title')).group().strip()
            , 'artist': re.search(r'^[^-]+', release.get('title')).group().strip()
            , 'year': release.get('year')
            , 'country': release.get('country')
            , 'catalog_number': release.get('catno')
            , 'barcode' : barcode
            , 'labels': ', '.join(map(str, release.get('label')))
            , 'genre': ', '.join(map(str, release.get('genre')))
            , 'sub_genre': ', '.join(map(str, release.get('style')))
            , 'format': release.get('formats')[0].get('name')
            , 'cover_url': release.get('cover_image')
        }

        albums.append(album)  

    return albums

@app.get("/album", response_model = List[AlbumSchema])
def show_albums(session: Session = Depends(get_session)):
    #show all albums.
    albums = session.query(Album).order_by(Album.artist, Album.album).all()

    return albums

@app.get("/album/{id}", response_model=AlbumSchema)
def show_album(id: int, session: Session = Depends(get_session)):
    #show album with id {x}.    
    album = session.query(Album).get(id)

    if not album:
        raise HTTPException(status_code=404, detail=f"Ops, we still dosen't have an album with id {id} :(")

    return album

@app.post("/album/", response_model=AlbumSchema, status_code=status.HTTP_201_CREATED)
def create_album(album_user: AlbumSchema, session: Session = Depends(get_session)):
    #create an album.
    album = Album(
        id = album_user.id
        , title = album_user.title
        , album = album_user.album
        , artist = album_user.artist
        , year = album_user.year
        , country = album_user.country
        , catalog_number = album_user.catalog_number
        , barcode = album_user.barcode
        , labels = album_user.labels
        , genre = album_user.genre
        , sub_genre = album_user.sub_genre
        , format = album_user.format
        , cover_url = album_user.cover_url
        , created_at = datetime.utcnow()
        , updated_at = datetime.utcnow()
    )

    session.add(album)
    session.commit()
    session.refresh(album)

    return album

@app.put("/album/{id}")
def update_album(id: int, album_user: AlbumSchema, session: Session = Depends(get_session)):
    #update album with id {x}.
    album = session.query(Album).get(id)

    if album:
        id = album_user.id
        title = album_user.title
        album = album_user.album
        artist = album_user.artist
        year = album_user.year
        country = album_user.country
        catalog_number = album_user.catalog_number
        barcode = album_user.barcode
        labels = album_user.labels
        genre = album_user.genre
        sub_genre = album_user.sub_genre
        format = album_user.format
        cover_url = album_user.cover_url
        created_at = album_user.created_at
        updated_at = datetime.utcnow()
        session.commit()

    if not album:
        raise HTTPException(status_code=404, detail=f"Ops, we still dosen't have an album with id {id} :(")

    return f"The album with ID {album.id} was updated!"

@app.delete("/album/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(id: int, session: Session = Depends(get_session)):
    #delete album with id {x].
    album = session.query(Album).get(id)

    if album:
        title = album.title
        session.delete(album)
        session.commit()
    
    if not album:
        raise HTTPException(status_code=404, detail=f"Ops, we still dosen't have an album with id {id} :(")

    #TO-DO: Fix "h11._util.LocalProtocolError: Too much data for declared Content-Length" error
    pass