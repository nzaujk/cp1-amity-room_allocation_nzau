from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import with_polymorphic

"""declare declarative base to enable mapping classes to the databse"""
Base = declarative_base


class AmityDatabaseSetup(object):
    def __init__(self, db_name='amity_db'):
        self.db_name = db_name
        if self.db_name:
            self.db_name = db_name + '.sqlite'
        else:
            self.db_name = 'default_amity_db.sqlite'
        self.engine = create_engine('sqlite:///' + self.db_name)
        self.session = sessionmaker(bind=self.engine)()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_name = Column(String(254), nullable=False)
    role = Column(String(64), nullable=False)
    type = Column(String(64))


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    room_name = Column(String(64), nullable=False)
    room_type = Column(String(64), nullable=False)


class Office(Base):
    __tablename__ = "office"
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(128), nullable=False)
    members = Column(String(250))


class LivingSpace(Base):
    __tablename__ = "living space"
    id = Column(Integer, primary_key=True,autoincrement=True)
    room_name = Column(String(128), nullable=False)
    members = Column(String(250))


class Unallocated(Base, Person):
    __tablename__ = "unallocated members"


Base.metadata.create_all(self.engine)