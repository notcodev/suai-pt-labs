from sqlalchemy.orm.session import Session
from src.schema import Song


class SongRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, title, artist, album, duration):
        song = Song(title=title, artist=artist, album=album, duration=duration)
        self.session.add(song)
        self.session.commit()
        return song

    def get_by_id(self, song_id):
        return self.session.query(Song).filter(Song.id == song_id).first()
