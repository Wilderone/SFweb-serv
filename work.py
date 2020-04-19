import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = 'sqlite:///albums.sqlite3'
Base = declarative_base()


class Album(Base):
    """Описывает структуру БД album"""

    __tablename__ = 'album'
    id = sa.Column(sa.Integer, primary_key=True)
    year = sa.Column(sa.Integer)
    artist = sa.Column(sa.Text)
    genre = sa.Column(sa.Text)
    album = sa.Column(sa.Text)

    def close(self):
        self.session.close()


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """Находит альбом по артисту"""
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def check_compare(new_alb):
    """Проверяет, существует ли такой альбом в списке.
    Проверка по исполнителю и названию альбома"""
    session = connect_db()
    albums = session.query(Album)
    for album in albums:
        if album.artist == new_alb.artist and album.album == new_alb.album:
            raise ValueError('Album already exists')
    return new_alb


def add(alb):
    """Добавляет запись в БД"""
    session = connect_db()
    new_album = alb
    session.add(check_compare(new_album))
    session.commit()
    print('Album Saved')
    return 'Album saved'
