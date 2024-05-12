from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

listener_station_association_table = Table('listener_stations', Base.metadata,
    Column('listener_id', Integer, ForeignKey('users.id')),
    Column('station_id', Integer, ForeignKey('stations.id'))
)

playlist_song_association_table = Table('playlist_songs', Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('song_id', Integer, ForeignKey('songs.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    playlists = relationship("Playlist", back_populates="user")
    stations = relationship("Station", secondary=listener_station_association_table, back_populates="listeners")

class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="playlists")
    songs = relationship("Song", secondary=playlist_song_association_table)

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album = Column(String)
    duration = Column(Integer, nullable=False)  # Duration in seconds

class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User")
    listeners = relationship("User", secondary=listener_station_association_table, back_populates="stations")
    current_playlist_id = Column(Integer, ForeignKey('playlists.id'))
    current_playlist = relationship("Playlist")
