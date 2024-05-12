from sqlalchemy.orm.session import Session
from src.repositories.playlist import PlaylistRepository
from src.repositories.song import SongRepository
from src.repositories.station import StationRepository
from src.repositories.user import UserRepository
from src.singleton import Singleton


class Repositories(metaclass=Singleton):
    def __init__(self, session: Session):
        self.playlist = PlaylistRepository(session)
        self.user = UserRepository(session)
        self.song = SongRepository(session)
        self.station = StationRepository(session)
