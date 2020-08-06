from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey, Float
)
from sqlalchemy.orm import mapper, relationship

from src.people.domain_models.models import Timezone, Coordinates, Location, User, \
    Person, LoginInfo, ContactInfo, PersonalId

metadata = MetaData()

user = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('date_registered', Date),
    Column('nat', String(50))
)

person = Table(
    'person', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('gender', String(20)),
    Column('title', String(2)),
    Column('first_name', String(50)),
    Column('second_name', String(50)),
    Column('date_of_birth', Date),
    Column('user_id', Integer, ForeignKey('user.id'))
)

login_info = Table(
    'login_info', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('uuid', String),
    Column('username', String(50)),
    Column('password', String),
    Column('salt', String),
    Column('md5', String),
    Column('sha1', String),
    Column('sha256', String),
    Column('user_id', Integer, ForeignKey('user.id'))
)

contact_info = Table(
    'contact_info', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('phone', String),
    Column('cell', String),
    Column('email', String),
    Column('user_id', Integer, ForeignKey('user.id'))
)

timezone = Table(
    'timezone', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('offset', String(10)),
    Column('description', String(30), unique=True),
)

coordinates = Table(
    'coordinates', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('latitude', Float),
    Column('longitude', Float),
)

location = Table(
    'location', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('street', String(50)),
    Column('city', String(50)),
    Column('state', String(50)),
    Column('postcode', String(5)),
    Column('timezone_id', Integer, ForeignKey('timezone.id')),
    Column('coordinates_id', Integer, ForeignKey('coordinates.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)

personal_id = Table(
    'personal_id', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('value', String),
    Column('user_id', Integer, ForeignKey('user.id'))
)


def start_mappers():
    location_mapper = mapper(Location, location)
    mapper(Timezone, timezone, properties={
        'locations': relationship(location_mapper, backref='timezone')
    })
    mapper(Coordinates, coordinates, properties={
        'locations': relationship(location_mapper, backref='coordinates')
    })

    person_mapper = mapper(Person, person)
    login_info_mapper = mapper(LoginInfo, login_info)
    contact_info_mapper = mapper(ContactInfo, contact_info)
    personal_id_mapper = mapper(PersonalId, personal_id)
    mapper(User, user, properties={
        'person': relationship(person_mapper, backref='user', uselist=False),
        'login_info': relationship(login_info_mapper, backref='user', uselist=False),
        'contact_info': relationship(contact_info_mapper, backref='user',
                                     uselist=False),
        'location': relationship(location_mapper, backref='user', uselist=False),
        'personal_id': relationship(personal_id_mapper, backref='user', uselist=False)
    })
