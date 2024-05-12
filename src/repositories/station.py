from sqlalchemy.orm.session import Session

from src.schema import Station


class StationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, name, description, owner_id):
        station = Station(name=name, description=description, owner_id=owner_id)
        self.session.add(station)
        self.session.commit()
        return station


    def get_by_id(self, station_id):
        return self.session.query(Station).filter(Station.id == station_id).first()
