from sqlalchemy.orm.session import Session
from src.schema import Playlist


class PlaylistRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, name, user_id):
        playlist = Playlist(name=name, user_id=user_id)
        self.session.add(playlist)
        self.session.commit()
        return playlist

    def get_by_id(self, playlist_id):
        return self.session.query(Playlist).filter(Playlist.id == playlist_id).first()
