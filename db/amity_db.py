from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session


Base = declarative_base()


class PersonDB(Base):
    """PersonDB will handle the table in the person class,"""
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(254), nullable=False)
    role = Column(String(64), nullable=False)


class RoomDB(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, nullable=False)
    room_name = Column(String(64), nullable=False)
    room_type = Column(String(64), nullable=False)


class OfficeDB(Base):
    __tablename__ = "office"
    id = Column(Integer, primary_key=True, nullable=False)
    room_name = Column(String(64), nullable=False)
    occupants = Column(String(128))


class LivingSpaceDB(Base):
    __tablename__ = "living_space"
    id = Column(Integer, primary_key=True, nullable=False)
    room_name = Column(String(64), nullable=False)
    occupants = Column(String(128))


class UnallocatedDB(Base):
    __tablename__ = "unallocated_members"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    role = Column(String(64), nullable=False)


class AllocatedDB(Base):
    __tablename__ = "allocated_members"
    id = Column(Integer, primary_key=True)
    name = Column(String(2128), nullable=False)
    role = Column(String(64), nullable=False)
    room_name = Column(String(128), nullable=False)
    room_type = Column(String(64), nullable=False)


class AmityDatabaseLoad(object):
    def __init__(self, db_name=None):
        self.db_name = db_name
        if self.db_name:
            self.db_name = db_name + ".sqlite"
        else:
            self.db_name = 'room_allocation_db.sqlite'
        # create an SQLEngine object to handle the connection
        self.engine = create_engine('sqlite:///' + self.db_name)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.db_session = Session()

        # create object to manage the tables
        Base.metadata.create_all(self.engine)





